
# After clone repository, you need to following these steps to run the code 


```bash
# Set up Python environment
virtualenv venv
source venv/bin/activate

# Install required Python libraries
pip install Flask elasticsearch pandas

```
## Run the monitoring script 
```bash
python3 test1_a.py
 ```
 ## Explanation
In the solution Python script for test1_a.py, the subprocess module is used to detect whether a specific service is running or not. This is achieved by invoking the systemctl is-active command for each service within a try-except block. If the service is active, the subprocess call succeeds, and the service status is considered "UP." In case of a subprocess.CalledProcessError (which occurs when the service is inactive), the status is set to "DOWN." 

## Run REST web service
please change credential to your ElasticSearch 
```bash
python3 test1_b.py
```
 ## Explanation 
In this Flask application, the script creates a simple RESTful web service for monitoring and querying the status of services stored in Elasticsearch. The /add endpoint accepts JSON payloads and adds them to an Elasticsearch index named 'application_status' with a document type 'service_status'. The /healthcheck endpoint retrieves the latest records for three specified services ('httpd', 'rabbitMQ', 'postgreSQL') from Elasticsearch and determines the overall status based on the individual service statuses. The /latest_record_status/<service_name> endpoint retrieves the latest status of a specific service from Elasticsearch. The script utilizes the Flask web framework for handling HTTP requests and responses, and the Elasticsearch Python client to interact with Elasticsearch. Additionally, error handling is implemented to gracefully handle exceptions during Elasticsearch queries.

## Run Data anaysis (recccomended to use notebook file)
```bash
python3 test3.py
```
 ## Explanation 
In this Python script, the Pandas library is employed to process a real estate sales dataset ('assignment data.csv'). The script reads the dataset into a Pandas DataFrame, then performs data cleaning and analysis. It calculates the average price per square foot across all properties and filters the dataset to include only those properties sold for less than the calculated average price per square foot. The resulting filtered dataset is written to a new CSV file named 'filtered-sales-data.csv'. Finally,  prints the how many record in original and filtered data .
