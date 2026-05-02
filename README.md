# Experimental Web Server for DDoS-like Traffic Project

## Overview
This project provides a simple Flask-based web server used as the experimental target for a student project on DDoS-like traffic, monitoring, and mitigation.

## Endpoints
- `/` : basic server response
- `/test` : simple text response
- `/data` : JSON response
- `/slow` : delayed response for latency testing
- `/health` : health-check endpoint
- `/compute` : CPU-intensive endpoint for stress testing

## Features
- Simple and lightweight Flask server
- Multiple endpoints with different behaviors
- Basic request logging
- Error handling for 404 and 500 errors

## Run Instructions

### 1. Start the Server
1. Install dependencies:
   `pip install -r requirements.txt`

2. Run the server:
   `python app.py`

3. The server will be available at:
   `http://127.0.0.1:5000/`

### 2. Run the Baseline Test
To measure the server's performance under normal traffic conditions, run the baseline testing script while the server is running.

1. Open a **new, separate** terminal window.

2. Navigate into the baseline test folder:
   `cd baseline_test`
   
3. Run the test script:
   `python baseline_test.py`

## Purpose in the Project
This server is the base infrastructure used for:
- baseline testing
- DDoS-like traffic simulation
- monitoring experiments
- mitigation analysis

