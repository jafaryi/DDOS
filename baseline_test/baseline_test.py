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

        # Calculate metrics
        avg_time = statistics.mean(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        
        results[endpoint] = {
            "avg_time_ms": round(avg_time, 2),
            "min_time_ms": round(min_time, 2),
            "max_time_ms": round(max_time, 2),
            "success_rate": (success_count / NUM_REQUESTS_PER_ENDPOINT) * 100
        }
        
        print(f"  Avg: {results[endpoint]['avg_time_ms']} ms | Max: {results[endpoint]['max_time_ms']} ms | Success: {results[endpoint]['success_rate']}%")

    end_total_time = time.time()
    total_duration = end_total_time - start_total_time
    rps = total_requests / total_duration

    print(f"\n--- Overall Baseline Metrics ---")
    print(f"Total Time: {round(total_duration, 2)} seconds")
    print(f"Average Requests Per Second (RPS): {round(rps, 2)}")
    
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
    
    # Save the chart as an image
    plt.savefig('baseline_chart.png')
    print("\nChart saved as 'baseline_chart.png'.")

if __name__ == "__main__":
    test_results = run_baseline_test()
    generate_chart(test_results)