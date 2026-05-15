# Experimental Web Server for DDoS-like Traffic Project

## Overview

This project provides a simple Flask-based web server used as the experimental target for a student project on DDoS-like traffic, monitoring, and mitigation.

The purpose of this server is to create a small, controlled web infrastructure that can be tested under different conditions:

- normal traffic
- DDoS-like high-rate traffic
- system monitoring
- mitigation using techniques such as rate limiting

This server is not designed for real production use. It is designed for a controlled lab environment and educational analysis.

---

## Project Structure

- `app.py` — main Flask web server
- `server_validation.py` — checks whether the server endpoints are working correctly
- `baseline_test/baseline_test.py` — measures normal traffic performance (Person 2)
- `attack_test.py` — controlled high-concurrency traffic simulation (Person 3)
- `requirements.txt` — project dependencies
- `logs/server.log` — request log file generated while the server is running
- `baseline_test/baseline_chart.png`, `baseline_test/baseline_table.png` — charts from the baseline test (generated when you run the baseline script from that folder)

---

## Endpoints

The server includes several endpoints with different purposes:

- `/` — basic server response
- `/test` — simple text response
- `/data` — JSON response similar to a simple API
- `/slow` — delayed response for latency testing
- `/health` — health-check endpoint for service availability
- `/compute` — CPU-intensive endpoint for stress and monitoring experiments

The `/compute` endpoint was added intentionally to create more visible CPU activity during later monitoring and stress-testing phases.

---

## Features

- Simple and lightweight Flask server
- Multiple endpoints with different behaviors
- Health-check endpoint for availability testing
- CPU-intensive endpoint for monitoring experiments
- Basic request logging
- Error handling for 404 and 500 errors
- Suitable target system for baseline, DDoS-like traffic, monitoring, and mitigation experiments

---

## Requirements

Install the required dependencies using:

```bash
pip install -r requirements.txt
```

---

## Run Instructions

### 1. Start the server

From the project root:

```bash
python app.py
```

The server listens on port 5000. For local experiments, use:

```text
http://127.0.0.1:5000/
```

You can try these in a browser:

```text
http://127.0.0.1:5000/
http://127.0.0.1:5000/health
http://127.0.0.1:5000/data
http://127.0.0.1:5000/compute
http://127.0.0.1:5000/slow
```

---

### 2. Validate the server infrastructure

With the server still running, open a **second** terminal at the project root and run:

```bash
python server_validation.py
```

This checks that endpoints return the expected HTTP status codes. It is not a performance test.

---

### 3. Run the baseline test (Person 2)

With the server still running, open another terminal:

```bash
cd baseline_test
python baseline_test.py
```

This measures average and max response time, success rate, and endpoint RPS under low-concurrency traffic. It writes `baseline_chart.png` and `baseline_table.png` in the `baseline_test` folder (current working directory).

---

### 4. Run the controlled attack simulation (Person 3)

With the server still running, open another terminal at the **project root** (not inside `baseline_test`):

```bash
python attack_test.py
```

Optional: stress a lighter endpoint instead of the default CPU-heavy `/compute`:

```bash
python attack_test.py --endpoint /health
python attack_test.py --endpoint /data
```

---

## Person 3 — Controlled DDoS-like Traffic Simulation

**Purpose:** Person 3 runs a **bounded, local-only** burst of concurrent HTTP GET requests against `http://127.0.0.1:5000` to observe latency, throughput, and failures under load. This mimics aspects of a DDoS-like flood in a **safe educational setting**.

**Safety:** Use this only against your own Flask instance on this machine. The script targets **127.0.0.1** only, uses fixed request counts, and uses moderate concurrency levels suitable for a laptop lab. Do not retarget it at external sites or shared infrastructure.

**How to run:**

1. Start the server: `python app.py`
2. Open a second terminal at the project root
3. Run: `python attack_test.py` (optional: `--endpoint /health` or `--endpoint /data`)

**Generated outputs** (under `results/person3_attack/`):

| File | Description |
|------|-------------|
| `attack_results.csv` | Tabular metrics per concurrency level |
| `attack_results.json` | Same data in JSON for tooling or reports |
| `attack_chart_avg_response_time.png` | Average response time vs concurrency |
| `attack_chart_rps.png` | Throughput (RPS) vs concurrency |
| `attack_table.png` | Summary table image of attack metrics |
| `person3_attack_report.txt` | Short narrative: scenario, observations, and comparison to baseline |

**Connection to baseline:** Person 2 measured normal baseline behavior. Person 3 measures behavior under a controlled high-concurrency request flood and compares it with the baseline numbers in the generated report.

---

## Purpose in the Project

This server is the base infrastructure used by the whole group. It supports:

- baseline testing
- DDoS-like traffic simulation
- CPU and memory monitoring
- mitigation analysis
- before-and-after comparison

**Roles:**

- **Person 1** — experimental web infrastructure and validation.
- **Person 2** — baseline performance testing.
- **Person 3** — controlled DDoS-like traffic simulation (this repo includes `attack_test.py`).
- **Person 4** — system monitoring under different traffic conditions.
- **Person 5** — mitigation (e.g. rate limiting) and before/after comparison.

---

## Test Results

### Baseline test (normal traffic)

Under normal traffic conditions, the web server was stable and responsive. The system was tested with standard, low-concurrency traffic and achieved a **100%** success rate across tested endpoints.

Overall throughput was about **76.53** requests per second (RPS). Endpoints such as `/`, `/data`, and `/health` showed low average latency (on the order of a few to ~10 ms in sample runs). The `/compute` endpoint had higher baseline latency (CPU-bound work) while still succeeding consistently in baseline runs.

These results establish a baseline before introducing simulated high-concurrency traffic. After running `attack_test.py`, compare `results/person3_attack/` artifacts with the baseline outputs in `baseline_test/`.

---

## Notes

This project is for **educational purposes only**. DDoS-like traffic must be generated only in a controlled local environment against this test server. The goal is to study effects on availability and performance—not to perform real attacks on external systems.
