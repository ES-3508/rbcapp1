import subprocess
import json
from datetime import datetime

# Define the services array with 3 services
services = ["httpd", "rabbitMQ", "postgreSQL"]
host_name = "host1"  # replace with hostname, assuming all the services are running on the same server

for service in services:
    try:
        # Use subprocess.run with check=True to raise an exception on non-zero exit code
        output = subprocess.run(["systemctl", "status", service], capture_output=True, check=True)
        status = output.stdout.decode().strip()

        # Check the output status
        if "inactive" in status:
            service_status = "DOWN"
        else:
            print("active")
            service_status = "UP"

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        json_payload = {
            "service_name": service,
            "service_status": service_status,
            "host_name": host_name
        }

        # Write json payload to a json file
        filename = f"{service}-status-{timestamp}.json"
        with open(filename, "w") as file:
            json.dump(json_payload, file)

    except subprocess.CalledProcessError as e:
        # Handle the error, e.output contains the error message
        print(f"Error checking status for {service}: {e}")
    except Exception as e:
        # Handle other exceptions
        print(f"An unexpected error occurred: {e}")
