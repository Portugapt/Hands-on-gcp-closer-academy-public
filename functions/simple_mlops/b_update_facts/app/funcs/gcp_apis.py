"""This module contains the functions that interact with the GCP APIs."""
from typing import Any, Dict

from google.cloud import bigquery, pubsub


def execute_query(
    BQ: bigquery.Client,
    job_config: bigquery.QueryJobConfig,
    query: str,
    location: str | None = None,
    job_id: str | None = None,
) -> bigquery.QueryJob:
    '''Execute a query with the desired job configuration.

    Args:
        BQ (bigquery.Client): The BigQuery client instance.
        job_config (bigquery.QueryJobConfig): The desired job configuration for the query execution.
        query (str): The query string to be executed.
        location (str, optional): The location where the query will be run. Defaults to None.
        job_id (str, optional): The ID of the job. Defaults to None.

    Returns:
        bigquery.QueryJob: A new query job instance.
    '''
    return BQ.query(
        query,
        job_config=job_config,
        job_id=job_id,
        location=location,
    )


def execute_query_result(
    BQ: bigquery.Client,
    query: str,
    job_config: bigquery.QueryJobConfig = bigquery.QueryJobConfig(
        dry_run=False, use_query_cache=True),
    job_id: str | None = None,
    location: str | None = None,
) -> Any:
    '''Executes a BigQuery query and returns the results.

    This function is an intermediate step between executing a query and
    holding the query results. It passes the default job configuration to
    the execute_query function.

    Args:
        BQ (google.cloud.bigquery.client.Client): A BigQuery client object.
        query (str): The query to execute.
        job_config (google.cloud.bigquery.job.QueryJobConfig, optional):
            The configuration for the query job. Defaults to a QueryJobConfig
            object with dry_run=False and use_query_cache=True.
        job_id (str, optional): The ID of the job. Defaults to None.
        location (str, optional): The location of the job. Defaults to None.

    Returns:
        The results of the query execution.
    '''
    return execute_query(
        BQ=BQ,
        query=query,
        job_config=job_config,
        job_id=job_id,
        location=location,
    ).result()


def pubsub_publish_message(
    PS: pubsub.PublisherClient,
    project_id: str,
    topic_id: str,
    message: str,
    attributes: Dict[str, str] = {},
) -> None:
    """Publishes a message to a Pub/Sub topic.

    Args:
        PS (pubsub.PublisherClient): The pubsub client.
        project_id (str): The ID of the project where the topic is located.
        topic_id (str): The ID of the topic.
        message (str): The message to publish.
        attributes (Dict[str, str], optional): The attributes of the message.
            Defaults to {}.
    """
    _topic = PS.topic_path(project_id, topic_id)

    PS.publish(
        topic=_topic,
        data=message.encode('utf-8'),
        **attributes,)
