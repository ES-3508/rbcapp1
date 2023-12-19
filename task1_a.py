import json
import subprocess
from datetime import datetime

services = ["httpd", "rabbitMQ", "postgreSQL"]
host_name = "host1"  # Assuming all services are on the same server

for service in services:
    status = "UP"
    try:
         # Check the service status
        subprocess.check_output(["systemctl", "is-active", "--quiet", service])
    except subprocess.CalledProcessError:
        status = "DOWN"

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    json_payload = {
        "service_name": service,
        "service_status": status,
        "host_name": host_name
    }

    print(status)
    filename = f"{service}-status-{timestamp}.json"
    with open(filename, "w") as file:
        json.dump(json_payload, file)

