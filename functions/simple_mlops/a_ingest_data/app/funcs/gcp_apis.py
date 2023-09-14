"""This module contains the functions that interact with the GCP APIs."""
import json
from typing import Any, Dict, Sequence

from google.cloud import bigquery, pubsub, storage


def storage_download_blob_as_string(
    CS: storage.Client,
    bucket_name: str,
    file_path: str,
) -> str:
    """
    Downloads a blob from a Google Cloud Storage bucket and returns its content as a string.

    Args:
        CS (google.cloud.storage.Client): A Google Cloud Storage client object.
        bucket_name (str): The name of the bucket.
        file_path (str): The location of the blob/file inside the bucket.

    Returns:
        str: A string with the file content.

    Raises:
        ValueError: If the blob does not exist.
    """
    # Getting the bucket
    bucket = CS.bucket(bucket_name)

    # Getting the blob
    blob = bucket.blob(file_path)

    if blob.exists():
        # Downloading the blob
        return blob.download_as_text()
    else:
        raise ValueError(f'Blob {file_path} does not exist.')


def bigquery_insert_json_row(
    BQ: bigquery.Client,
    table_fqn: str,
    row: Sequence[Dict[str, Any]],
) -> Any:
    """Inserts a row into a bigquery table.

    Args:
        BQ (bigquery.Client): The bigquery client.
        table_fqn (str): The fully qualified name of the table.
        row (Dict[str, Any]): The row to insert into the table.
    """
    def _filter_dict(d: Dict[str, str]) -> Dict[str, str]:
        return {k: v for k, v in d.items() if isinstance(v, str) and bool(v.strip())}

    if not isinstance(row, Sequence) and isinstance(row, Dict):
        row = [row]

    errors = BQ.insert_rows_json(
        table=table_fqn,
        json_rows=[_filter_dict(d=d) for d in row],
    )

    if errors:
        print(json.dumps({'message': errors, 'severity': 'ERROR'}))
        return errors
    else:
        return None


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
