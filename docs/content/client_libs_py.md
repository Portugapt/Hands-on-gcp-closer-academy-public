
# Client Libraries

A client implementation, such as a Python Client or Javascript Client, is a software library designed to facilitate communication and interaction between an application and a specific service, like an API. It allows developers to easily access and utilize the service's functionalities, by abstracting low-level details and providing a more user-friendly interface in the language of choice.

The client implementation acts as an API layer between the application and the server, enabling seamless data exchange and requests management. This layer simplifies the process of making API calls, handling authentication, managing connection details, and processing responses from the server.

For example, the Google Cloud Platform (GCP) offers BigQuery Python Client and Python Cloud Storage as part of their Cloud Client Libraries. These libraries provide high-level API abstractions that significantly reduce the amount of boilerplate code developers need to write when interacting with BigQuery and Cloud Storage services.

Using the GCP BigQuery Python Client, developers can easily query, manage, and load data into BigQuery tables, while the Python Cloud Storage library simplifies file management, uploads, and downloads in Google Cloud Storage. Both libraries embrace the idiomatic style of the Python language, ensuring better integration with the standard library and developers' existing codebases.

You can check all the available Client Libraries for python [here](https://cloud.google.com/python/docs/reference).

## Bigquery Client (Python)

You can use the BigQuery Python Client to execute a query and fetch the results:

```python
# NOTE: pip install google-cloud-bigquery

from google.cloud import bigquery

# Initialize the BigQuery client
client = bigquery.Client()

# Define your query
query = """
    SELECT name, SUM(number) as total
    FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE year >= 2000
    GROUP BY name
    ORDER BY total DESC
    LIMIT 10
"""

# Execute the query
query_job = client.query(query)

# Fetch and print the results
for row in query_job.result():
    print(f"{row.name}: {row.total}")
```

## Cloud Storage Client (Python)

You can use the Python Cloud Storage Client to upload a file to a GCS bucket and download it back:

```python
# NOTE: pip install google-cloud-storage

from google.cloud import storage

# Initialize the GCS client
client = storage.Client()

# Specify your bucket name
bucket_name = "your-bucket-name"

# Get a reference to the bucket
bucket = client.get_bucket(bucket_name)

# Upload a file
source_file_name = "path/to/your/local/file.txt"
destination_blob_name = "uploaded_file.txt"
blob = bucket.blob(destination_blob_name)
blob.upload_from_filename(source_file_name)
print(f"File {source_file_name} uploaded to {destination_blob_name}.")

# Download the file
downloaded_file_name = "path/to/your/local/downloaded_file.txt"
blob = bucket.blob(destination_blob_name)
blob.download_to_filename(downloaded_file_name)
print(f"File {destination_blob_name} downloaded to {downloaded_file_name}.")
```


## Pub/Sub Client (Python)

You can use the Pub/Sub Python Client to publish a message to the existing topic:

```python
# NOTE: pip install google-cloud-pubsub

from google.cloud import pubsub_v1

# Initialize the Pub/Sub client
publisher = pubsub_v1.PublisherClient()

# Set your project_id and topic_name
project_id = "your-project-id"
topic_name = "your-existing-topic-name"

# Get the topic path
topic_path = publisher.topic_path(project_id, topic_name)

# Publish a message
message = "Hello, World!"
message_data = message.encode("utf-8")
future = publisher.publish(topic_path, message_data)
message_id = future.result()
print(f"Message published with ID: {message_id}")
```

As Pub/Sub promotes decoupled and flexible architectures, message_data is transformed into a [base64-encoded string](https://cloud.google.com/pubsub/docs/reference/rest/v1/PubsubMessage) to ensure language-agnostic compatibility. Therefore, subscribers must decode the base64 message. In Python, this can be done as follows:

```python
import base64

def hello_pubsub(data, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    print("This Function was triggered by messageId {} published at {}".format(context.event_id, context.timestamp))

    if 'data' in event:
        decoded_msg = base64.b64decode(data['data']).decode('utf-8')
        # Message is now decoded
    ## Your Cloud Function Implementation
```

## Setup python venv

```python
python -m venv venv
```

Install the Python Extension:

![img-py1](https://i.imgur.com/8JlFCFw.png)

With VSCode, do `CTRL+SHIFT+P` and write `Select Interpreter`

![img-py2](https://i.imgur.com/1Ul2HfI.png)

And find the `venv` python executable.

![img-py3](https://i.imgur.com/ULm24gE.png)
