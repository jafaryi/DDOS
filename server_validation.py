import requests

BASE_URL = "http://127.0.0.1:5000"

endpoints = {
    "/": 200,
    "/health": 200,
    "/data": 200,
    "/compute": 200,
    "/slow": 200,
    "/wrong": 404
}

print("Checking server endpoints...\n")

all_passed = True

for endpoint, expected_status in endpoints.items():
    url = BASE_URL + endpoint

    try:
        response = requests.get(url, timeout=5)
        status = response.status_code

        if status == expected_status:
            print(f"{endpoint:10} OK - {status}")
        else:
            print(f"{endpoint:10} FAILED - expected {expected_status}, got {status}")
            all_passed = False

    except requests.exceptions.RequestException as error:
        print(f"{endpoint:10} FAILED - {error}")
        all_passed = False

if all_passed:
    print("\nServer validation completed successfully.")
else:
    print("\nServer validation failed. Please check the server.")