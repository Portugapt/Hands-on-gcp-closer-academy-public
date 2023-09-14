"""This module contains named tuples for the update_facts function.

The module contains two named tuples: GCPClients and EnvVars. GCPClients is a named tuple containing
instances of Google Cloud Platform clients for interacting with BigQuery and Pub/Sub. EnvVars is a named tuple
containing environment variables required for the update_facts function.
"""

from typing import NamedTuple

from google.cloud import bigquery, pubsub


class GCPClients(NamedTuple):
    """A named tuple containing GCP client instances.

    Attributes:
        bigquery_client (google.cloud.bigquery.client.Client): A client for interacting with BigQuery.
        publisher (google.cloud.pubsub_v1.PublisherClient): A client for interacting with Pub/Sub.
    """
    bigquery_client: bigquery.Client
    publisher: pubsub.PublisherClient


class EnvVars(NamedTuple):
    """NamedTuple containing environment variables required for the update_facts function.

    Attributes:
        gcp_project_id (str): The ID of the Google Cloud Platform project.
        bq_facts_table_fqn (str): The fully-qualified name of the BigQuery table containing facts data.
        bq_staging_table_fqn (str): The fully-qualified name of the BigQuery table containing staging data.
        topic_update_facts_complete (str): The name of the Pub/Sub topic to publish a message to when the update_facts function completes.
    """
    gcp_project_id: str
    bq_facts_table_fqn: str
    bq_staging_table_fqn: str
    topic_update_facts_complete: str
