"""
Person 3 — Controlled DDoS-like traffic simulation (educational lab only).

This script sends a bounded burst of concurrent HTTP GET requests only to the
local Flask server at 127.0.0.1:5000. It is intended to observe how the server
behaves under high concurrency compared to the Person 2 baseline.

Safety:
- Targets only http://127.0.0.1:5000 (no external hosts).
- Fixed total requests per level; no infinite loops.
- Moderate concurrency levels suitable for a laptop lab.
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Non-interactive backend for saving PNG files safely
import matplotlib.pyplot as plt  # noqa: E402
import requests  # noqa: E402

# ---------------------------------------------------------------------------
# Lab configuration — local server only
# ---------------------------------------------------------------------------
BASE_URL = "http://127.0.0.1:5000"
ALLOWED_ENDPOINTS = ("/compute", "/health", "/data")
DEFAULT_ENDPOINT = "/compute"
CONCURRENCY_LEVELS = (5, 10, 25, 50)
TOTAL_REQUESTS_PER_LEVEL = 200
REQUEST_TIMEOUT_SEC = 5
RESULTS_DIR = Path("results") / "person3_attack"

# Person 2 baseline reference numbers (for written comparison in the report)
BASELINE_REFERENCE = {
    "success_rate_pct": 100.0,
    "overall_rps": 76.53,
    "avg_response_ms": {
        "/": 9.92,
        "/data": 10.25,
        "/health": 7.5,
        "/compute": 38.45,
    },
    "compute_max_ms": 61.86,
    "compute_endpoint_rps": 26.01,
}


def _validate_endpoint(endpoint: str) -> str:
    if endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(
            f"Endpoint must be one of {ALLOWED_ENDPOINTS}, got {endpoint!r}"
        )
    return endpoint


def _single_get(url: str) -> tuple[bool, float]:
    """
    Perform one GET request. Returns (success, elapsed_ms).
    Elapsed time is always measured for the attempt (including failures).
    """
    t0 = time.perf_counter()
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT_SEC)
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        ok = response.status_code == 200
        return ok, elapsed_ms
    except requests.exceptions.RequestException:
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        return False, elapsed_ms


def run_attack_level(url: str, concurrency: int, total_requests: int) -> dict:
    """
    Run a fixed number of concurrent GET requests using ThreadPoolExecutor.
    Measures latency and success for each concurrency scenario.
    """
    successes = 0
    failures = 0
    times_ms: list[float] = []

    wall_t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(_single_get, url) for _ in range(total_requests)]
        for fut in as_completed(futures):
            ok, elapsed_ms = fut.result()
            times_ms.append(elapsed_ms)
            if ok:
                successes += 1
            else:
                failures += 1
    wall_elapsed = time.perf_counter() - wall_t0

    total = successes + failures
    success_rate = (successes / total * 100.0) if total else 0.0
    rps = total / wall_elapsed if wall_elapsed > 0 else 0.0

    avg_ms = statistics.mean(times_ms) if times_ms else 0.0
    min_ms = min(times_ms) if times_ms else 0.0
    max_ms = max(times_ms) if times_ms else 0.0

    return {
        "tested_endpoint": url.replace(BASE_URL, "") or "/",
        "concurrency": concurrency,
        "total_requests": total,
        "successful_requests": successes,
        "failed_requests": failures,
        "success_rate_pct": round(success_rate, 2),
        "avg_response_time_ms": round(avg_ms, 2),
        "min_response_time_ms": round(min_ms, 2),
        "max_response_time_ms": round(max_ms, 2),
        "requests_per_second": round(rps, 2),
    }


def ensure_server_reachable(base_url: str) -> None:
    """Quick check so students get a clear message if the server is down."""
    try:
        r = requests.get(f"{base_url}/health", timeout=2)
        if r.status_code != 200:
            print("Warning: /health did not return 200. Continuing anyway.")
    except requests.exceptions.RequestException as e:
        raise SystemExit(
            "Could not reach the local server at http://127.0.0.1:5000.\n"
            "Start it first in another terminal: python app.py\n"
            f"Details: {e}"
        ) from e


def write_csv(rows: list[dict], path: Path) -> None:
    if not rows:
        return
    fieldnames = [
        "tested_endpoint",
        "concurrency",
        "total_requests",
        "successful_requests",
        "failed_requests",
        "success_rate_pct",
        "avg_response_time_ms",
        "min_response_time_ms",
        "max_response_time_ms",
        "requests_per_second",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_json(rows: list[dict], path: Path) -> None:
    payload = {
        "description": "Person 3 controlled high-concurrency GET flood (local lab)",
        "base_url": BASE_URL,
        "results": rows,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def plot_avg_response_vs_concurrency(rows: list[dict], path: Path) -> None:
    conc = [r["concurrency"] for r in rows]
    avgs = [r["avg_response_time_ms"] for r in rows]
    plt.figure(figsize=(8, 5))
    plt.plot(conc, avgs, marker="o", color="darkred", linewidth=2)
    plt.title("Attack simulation: average response time vs concurrency")
    plt.xlabel("Concurrency (worker threads)")
    plt.ylabel("Average response time (ms)")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()


def plot_rps_vs_concurrency(rows: list[dict], path: Path) -> None:
    conc = [r["concurrency"] for r in rows]
    rps = [r["requests_per_second"] for r in rows]
    plt.figure(figsize=(8, 5))
    plt.plot(conc, rps, marker="s", color="navy", linewidth=2)
    plt.title("Attack simulation: throughput (RPS) vs concurrency")
    plt.xlabel("Concurrency (worker threads)")
    plt.ylabel("Requests per second (all attempts)")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()


def generate_summary_table_image(rows: list[dict], path: Path) -> None:
    columns = (
        "Concurrency",
        "Total",
        "OK",
        "Fail",
        "Success %",
        "Avg ms",
        "Min ms",
        "Max ms",
        "RPS",
    )
    cell_text = []
    for r in rows:
        cell_text.append(
            [
                r["concurrency"],
                r["total_requests"],
                r["successful_requests"],
                r["failed_requests"],
                f"{r['success_rate_pct']}%",
                r["avg_response_time_ms"],
                r["min_response_time_ms"],
                r["max_response_time_ms"],
                r["requests_per_second"],
            ]
        )
    fig, ax = plt.subplots(figsize=(11, 3.5))
    ax.axis("tight")
    ax.axis("off")
    table = ax.table(
        cellText=cell_text, colLabels=columns, loc="center", cellLoc="center"
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.9)
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight="bold")
            cell.set_facecolor("#e0e0e0")
    ep = rows[0]["tested_endpoint"] if rows else ""
    plt.title(f"Attack metrics summary — endpoint {ep}", pad=16, weight="bold")
    plt.savefig(path, bbox_inches="tight", dpi=200)
    plt.close()


def write_report(rows: list[dict], endpoint: str, path: Path) -> None:
    """Short narrative report with measured numbers and baseline comparison."""
    br = BASELINE_REFERENCE
    baseline_avg = br["avg_response_ms"].get(endpoint, None)

    lines = []
    lines.append("Person 3 — Controlled DDoS-like Traffic Simulation Report")
    lines.append("=" * 60)
    lines.append("")
    lines.append("1. Attack scenario description")
    lines.append("-" * 40)
    lines.append(
        "This lab simulates a controlled, high-concurrency HTTP GET flood against "
        "the group's own Flask server on 127.0.0.1:5000. Each scenario issues a "
        f"fixed batch of {TOTAL_REQUESTS_PER_LEVEL} requests using ThreadPoolExecutor "
        "with a set worker count (concurrency). The goal is to observe latency, "
        "throughput, and error behavior under load—not to attack any external system."
    )
    lines.append("")
    lines.append("2. Tested endpoint")
    lines.append("-" * 40)
    lines.append(f"  {endpoint}  (full URL: {BASE_URL}{endpoint})")
    lines.append("")
    lines.append("3. Traffic levels (concurrency)")
    lines.append("-" * 40)
    lines.append(f"  Concurrency values tested: {', '.join(map(str, CONCURRENCY_LEVELS))}")
    lines.append(f"  Total requests per level: {TOTAL_REQUESTS_PER_LEVEL}")
    lines.append("")
    lines.append("4. What happened during the attack (measured)")
    lines.append("-" * 40)
    for r in rows:
        lines.append(
            f"  Concurrency {r['concurrency']:>2}: success {r['success_rate_pct']}% | "
            f"avg {r['avg_response_time_ms']} ms | max {r['max_response_time_ms']} ms | "
            f"RPS {r['requests_per_second']} | failed {r['failed_requests']}"
        )
    lines.append("")
    lines.append("5. First comparison with Person 2 baseline")
    lines.append("-" * 40)
    lines.append(
        f"Baseline (normal traffic) success rate was {br['success_rate_pct']}%. "
        f"Overall baseline throughput was about {br['overall_rps']} RPS across endpoints."
    )
    if baseline_avg is not None:
        lines.append(
            f"For this endpoint, baseline average response time was about {baseline_avg} ms."
        )
    if endpoint == "/compute":
        lines.append(
            f"Baseline /compute also had max latency about {br['compute_max_ms']} ms and "
            f"endpoint RPS about {br['compute_endpoint_rps']} under low-concurrency testing."
        )
    worst = max(rows, key=lambda x: x["avg_response_time_ms"])
    best_rps = max(rows, key=lambda x: x["requests_per_second"])
    lines.append(
        f"In this run, highest average latency was at concurrency {worst['concurrency']} "
        f"({worst['avg_response_time_ms']} ms). "
        f"Highest throughput (RPS) among tested levels was {best_rps['requests_per_second']} "
        f"at concurrency {best_rps['concurrency']}."
    )
    lines.append(
        "Compared with the baseline, the DDoS-like request flood increased response time "
        "and changed stability/throughput depending on concurrency level. The /compute "
        "endpoint is affected more strongly than light endpoints because it performs "
        "CPU-intensive work per request, so many overlapping calls queue and compete for CPU."
    )
    lines.append("")
    lines.append("6. Conclusion")
    lines.append("-" * 40)
    lines.append(
        "The local server shows measurable stress under concurrent load: latencies rise "
        "and some requests may fail or time out as contention increases. "
        "Use these artifacts alongside baseline_test output for before/under-load analysis."
    )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Person 3 local high-concurrency GET simulation (127.0.0.1 only)."
    )
    parser.add_argument(
        "--endpoint",
        default=DEFAULT_ENDPOINT,
        choices=list(ALLOWED_ENDPOINTS),
        help="Path to stress (default: CPU-heavy /compute).",
    )
    args = parser.parse_args()
    endpoint = _validate_endpoint(args.endpoint)
    url = f"{BASE_URL}{endpoint}"

    ensure_server_reachable(BASE_URL)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print("Person 3 attack simulation (local lab only)")
    print(f"Target: {url}")
    print(f"Requests per concurrency level: {TOTAL_REQUESTS_PER_LEVEL}")
    print(f"Concurrency levels: {CONCURRENCY_LEVELS}")
    print()

    rows: list[dict] = []
    for conc in CONCURRENCY_LEVELS:
        print(f"Running concurrency={conc} ...")
        row = run_attack_level(url, conc, TOTAL_REQUESTS_PER_LEVEL)
        rows.append(row)
        print(
            f"  -> success {row['success_rate_pct']}% | avg {row['avg_response_time_ms']} ms | "
            f"RPS {row['requests_per_second']}"
        )

    csv_path = RESULTS_DIR / "attack_results.csv"
    json_path = RESULTS_DIR / "attack_results.json"
    chart_avg_path = RESULTS_DIR / "attack_chart_avg_response_time.png"
    chart_rps_path = RESULTS_DIR / "attack_chart_rps.png"
    table_path = RESULTS_DIR / "attack_table.png"
    report_path = RESULTS_DIR / "person3_attack_report.txt"

    write_csv(rows, csv_path)
    write_json(rows, json_path)
    plot_avg_response_vs_concurrency(rows, chart_avg_path)
    plot_rps_vs_concurrency(rows, chart_rps_path)
    generate_summary_table_image(rows, table_path)
    write_report(rows, endpoint, report_path)

    print()
    print("Saved:")
    print(f"  {csv_path}")
    print(f"  {json_path}")
    print(f"  {chart_avg_path}")
    print(f"  {chart_rps_path}")
    print(f"  {table_path}")
    print(f"  {report_path}")


if __name__ == "__main__":
    main()
