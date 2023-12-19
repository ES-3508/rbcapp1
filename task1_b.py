from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])  # Replace with your Elasticsearch configuration

index_name='application_status'

@app.route('/add', methods=['POST'])
def add_to_elasticsearch():
    data = request.get_json()
    es.index(index=index_name, doc_type='service_status', body=data)
    return jsonify({"message": "Data added to Elasticsearch"}), 201

@app.route('/healthcheck', methods=['GET'])
def get_overall_status():
    try:
        # Elasticsearch query to retrieve the latest records for three services
        query = {
            "size": 3,
            "sort": [{"@timestamp": {"order": "desc"}}],
            "query": {
                "bool": {
                    "should": [
                        {"term": {"service_name": "httpd"}},
                        {"term": {"service_name": "rabbitMQ"}},
                        {"term": {"service_name": "postgreSQL"}}
                    ]
                }
            }
        }

        # Execute the query
        response = es.search(index=index_name, body=query)

        # Extract the statuses of the three services
        httpd_status = get_service_status(response, "httpd")
        rabbitmq_status = get_service_status(response, "rabbitMQ")
        postgresql_status = get_service_status(response, "postgreSQL")

        # Determine the overall status
        overall_status = "UP" if all(status == "UP" for status in [httpd_status, rabbitmq_status, postgresql_status]) else "DOWN"

        return jsonify({"overall_status": overall_status})

    except Exception as e:
        return jsonify({"message": f"Error querying Elasticsearch: {str(e)}"}), 500



@app.route('/latest_record_status/<service_name>', methods=['GET'])
def get_latest_record_status(service_name):
    try:
        # Elasticsearch query to retrieve the latest document for a specific service
        query = {
            "size": 1,
            "sort": [{"@timestamp": {"order": "desc"}}],
            "query": {
                "bool": {
                    "must": [{"match": {"service_name": service_name}}]
                }
            }
        }

        # Execute the query
        response = es.search(index=index_name, body=query)

        # Extract and return the status of the latest record
        if response['hits']['hits']:
            latest_record_status = response['hits']['hits'][0]['_source'].get('service_status')
            if latest_record_status:
                return jsonify({"latest_record_status": latest_record_status})
            else:
                return jsonify({"message": f"No status information found for {service_name}."}), 404
        else:
            return jsonify({"message": f"No records found for service {service_name} in the specified index."}), 404

    except Exception as e:
        return jsonify({"message": f"Error querying Elasticsearch: {str(e)}"}), 500


def get_service_status(response, service_name):
    hits = response['hits']['hits']
    for hit in hits:
        if hit['_source']['service_name'] == service_name:
            service_status = hit['_source'].get('service_status')
            if service_status == "UP":
                return "UP"
    return "DOWN"  # If no record found for the service status assume "DOWN"


if __name__ == '__main__':
    app.run(debug=True)

