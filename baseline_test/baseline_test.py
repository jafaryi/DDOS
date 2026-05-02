import requests
import time
import statistics
import matplotlib.pyplot as plt

# Configuration
BASE_URL = "http://127.0.0.1:5000"
ENDPOINTS = ["/", "/data", "/health", "/compute"]
NUM_REQUESTS_PER_ENDPOINT = 50  # Simulating normal, low-concurrency traffic

def run_baseline_test():
    print("Starting Baseline Test...")
    results = {}
    total_requests = 0
    start_total_time = time.time()

    for endpoint in ENDPOINTS:
        url = f"{BASE_URL}{endpoint}"
        print(f"\nTesting {url}...")
        
        response_times = []
        success_count = 0
        
        # Track time specifically for this endpoint's RPS
        start_ep_time = time.time()
        
        for _ in range(NUM_REQUESTS_PER_ENDPOINT):
            start_req_time = time.time()
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    success_count += 1
            except requests.exceptions.RequestException:
                pass
            
            end_req_time = time.time()
            response_times.append((end_req_time - start_req_time) * 1000) # Convert to ms
            total_requests += 1

        end_ep_time = time.time()
        ep_duration = end_ep_time - start_ep_time
        
        # Calculate Endpoint RPS
        endpoint_rps = NUM_REQUESTS_PER_ENDPOINT / ep_duration if ep_duration > 0 else 0

        # Calculate other metrics
        avg_time = statistics.mean(response_times) if response_times else 0
        min_time = min(response_times) if response_times else 0
        max_time = max(response_times) if response_times else 0
        
        results[endpoint] = {
            "avg_time_ms": round(avg_time, 2),
            "max_time_ms": round(max_time, 2),
            "success_rate": (success_count / NUM_REQUESTS_PER_ENDPOINT) * 100,
            "endpoint_rps": round(endpoint_rps, 2)
        }
        
        print(f"  Avg: {results[endpoint]['avg_time_ms']} ms | RPS: {results[endpoint]['endpoint_rps']} | Success: {results[endpoint]['success_rate']}%")

    end_total_time = time.time()
    total_duration = end_total_time - start_total_time
    overall_rps = total_requests / total_duration

    print(f"\n--- Overall Baseline Metrics ---")
    print(f"Total Time: {round(total_duration, 2)} seconds")
    print(f"Overall Requests Per Second (RPS): {round(overall_rps, 2)}")
    
    return results

def generate_chart(results):
    endpoints = list(results.keys())
    avg_times = [results[ep]["avg_time_ms"] for ep in endpoints]

    plt.figure(figsize=(10, 6))
    plt.bar(endpoints, avg_times, color='skyblue')
    plt.title('Baseline Response Times by Endpoint')
    plt.xlabel('Endpoints')
    plt.ylabel('Average Response Time (ms)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('baseline_chart.png')
    plt.close() # Close figure to avoid memory leaks
    print("\nChart saved as 'baseline_chart.png'.")

def generate_table(results):
    endpoints = list(results.keys())
    columns = ("Endpoint", "Avg Time (ms)", "Max Time (ms)", "Success Rate (%)", "Endpoint RPS")
    cell_text = []

    for ep in endpoints:
        cell_text.append([
            ep,
            results[ep]["avg_time_ms"],
            results[ep]["max_time_ms"],
            f"{results[ep]['success_rate']}%",
            results[ep]["endpoint_rps"]
        ])

    fig, ax = plt.subplots(figsize=(9, 4))
    
    # Hide axes
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=cell_text, colLabels=columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.8) # Adjust row height

    # Style the header row
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight='bold')
            cell.set_facecolor('#e0e0e0')

    plt.title('Baseline Performance Metrics', pad=20, weight='bold')
    plt.savefig('baseline_table.png', bbox_inches='tight', dpi=300) # High-res export
    plt.close()
    print("Table saved as 'baseline_table.png'.")

if __name__ == "__main__":
    test_results = run_baseline_test()
    generate_chart(test_results)
    generate_table(test_results)