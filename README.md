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

- `app.py` : main Flask web server
- `server_validation.py` : checks whether the server endpoints are working correctly
- `baseline_test.py` : measures normal traffic performance
- `requirements.txt` : project dependencies
- `logs/server.log` : request log file generated while the server is running
- `baseline_chart.png` : chart generated from the baseline test

---

## Endpoints

The server includes several endpoints with different purposes:

- `/` : basic server response
- `/test` : simple text response
- `/data` : JSON response similar to a simple API
- `/slow` : delayed response for latency testing
- `/health` : health-check endpoint for service availability
- `/compute` : CPU-intensive endpoint for stress and monitoring experiments

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
<<<<<<< HEAD
=======

### 1. Start the Server
1. Install dependencies:
   `pip install -r requirements.txt`
>>>>>>> fc9201bc3912739e5040d8d5acdbcad41769a7b0

### 1. Start the Server

<<<<<<< HEAD
Run the Flask server:

```bash
python app.py
```

The server will be available at:

```text
http://127.0.0.1:5000/
```

You can test the server manually in a browser using:

```text
http://127.0.0.1:5000/
http://127.0.0.1:5000/health
http://127.0.0.1:5000/data
http://127.0.0.1:5000/compute
http://127.0.0.1:5000/slow
```

---

### 2. Validate the Server Infrastructure

Before running performance experiments, the server can be validated to make sure all endpoints are working correctly.

Open a new terminal while the server is still running, then run:

```bash
python server_validation.py
```

The validation script checks whether the implemented endpoints return the expected HTTP status codes.

Expected validation output:

```text
Checking server endpoints...

/          OK - 200
/health    OK - 200
/data      OK - 200
/compute   OK - 200
/slow      OK - 200
/wrong     OK - 404

Server validation completed successfully.
```

This validation step is not a performance test.  
It only confirms that the web server infrastructure is working correctly and is ready for the next phases of the project.

---

### 3. Run the Baseline Test

To measure the server's performance under normal traffic conditions, run the baseline testing script while the server is running.

Open a new terminal and run:

```bash
python baseline_test.py
```

The baseline test measures:

- average response time
- minimum response time
- maximum response time
- success rate
- overall requests per second

It also generates a chart named:

```text
baseline_chart.png
```

---

## Test Results

### Baseline Test: Normal Traffic Condition

Under normal traffic conditions, the web server was stable and responsive.

The system was tested with standard, low-concurrency traffic and achieved a 100% success rate across all tested endpoints.

The overall throughput was:

```text
76.53 Requests Per Second
```

Standard endpoints such as `/`, `/data`, and `/health` performed very well, with average response times around 2–6 ms.

The `/compute` endpoint had a higher baseline latency of about 40 ms because it includes an intentional CPU loop. However, it still responded successfully in every test.

These results establish a healthy baseline before introducing the simulated DDoS-like traffic.

---
=======
3. The server will be available at:
   `http://127.0.0.1:5000/`
>>>>>>> fc9201bc3912739e5040d8d5acdbcad41769a7b0

### 2. Run the Baseline Test
To measure the server's performance under normal traffic conditions, run the baseline testing script while the server is running.

1. Open a **new, separate** terminal window.

2. Navigate into the baseline test folder:
   `cd baseline_test`
   
3. Run the test script:
   `python baseline_test.py`

## Purpose in the Project

This server is the base infrastructure used by the whole group.

It supports:

- baseline testing
- DDoS-like traffic simulation
- CPU and memory monitoring
- mitigation analysis
- before-and-after comparison

<<<<<<< HEAD
Person 1 is responsible for creating and validating this experimental web infrastructure.

Person 2 uses this server for baseline performance testing.

Person 3 uses this server as the target for controlled DDoS-like traffic simulation.

Person 4 monitors the system behavior while the server is under different traffic conditions.

Person 5 applies mitigation techniques such as rate limiting and compares the results before and after mitigation.

---

## Notes

This project is designed for educational purposes only.

The DDoS-like traffic used in this project must be generated only in a controlled local environment against our own test server.

The goal is not to perform a real cyberattack, but to study how high-rate traffic affects availability, performance, and resilience in a small web infrastructure.
=======
## Test results

### 1. Baseline test (no attack)
Under normal traffic conditions, the web server is highly stable and responsive. 
We tested the system with standard, low-concurrency traffic and achieved a 100% success rate across all endpoints.

The overall throughput was 76.53 Requests Per Second (RPS).
Standard endpoints like /, /data, and /health performed exceptionally well, with average response times around 2-6 ms. 
As expected by the design, the /compute endpoint had a higher baseline latency of about 40 ms due to the intentional CPU loop, but it still resolved successfully every time. 
This establishes a healthy, functioning baseline before we introduce the simulated attack.

>>>>>>> fc9201bc3912739e5040d8d5acdbcad41769a7b0
