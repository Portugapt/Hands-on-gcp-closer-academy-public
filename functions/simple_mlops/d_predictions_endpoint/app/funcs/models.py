"""Models for the ingest_data function. Simplifies type hinting."""
from typing import NamedTuple

from google.cloud import bigquery, storage


class GCPClients(NamedTuple):
    """
    A named tuple that contains clients for Google Cloud Platform services.

    Attributes:
        storage_client (google.cloud.storage.Client): A client for Google Cloud Storage.
        bigquery_client (google.cloud.bigquery.Client): A client for Google BigQuery.
        publisher (google.cloud.pubsub_v1.PublisherClient): A client for Google Cloud Pub/Sub.
    """
    storage_client: storage.Client
    bigquery_client: bigquery.Client


class EnvVars(NamedTuple):
    """
    A named tuple representing environment variables used in the model training process.

    Attributes:
        gcp_project_id (str): The ID of the Google Cloud Platform project.
        bucket_name (str): The name of the Google Cloud Storage bucket where the model artifacts will be stored.
        model_location (str): The location of the trained model within the Google Cloud Storage bucket.
        predictions_table (str): The name of the BigQuery table where prediction results will be stored.
    """
    gcp_project_id: str
    bucket_name: str
    model_location: str
    predictions_table: str
