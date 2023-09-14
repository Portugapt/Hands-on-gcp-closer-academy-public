from io import BytesIO

import joblib
import pandas as pd
from google.cloud import bigquery, storage
from sklearn.pipeline import Pipeline


def _storage_write_bytes_file_to_bucket(
    CS: storage.Client,
    bucket_name: str,
    model_name: str,
    model_content: bytes,
    content_type: str = 'text/plain',
) -> None:
    """
    Uploads a file to a Google Cloud Storage bucket.

    Args:
        bucket_name (str): The name of the bucket to upload the file to.
        model_name (str): The name of the file to upload.
        model_content (bytes): The contents of the file to upload.
        content_type (str, optional): The content type of the file. Defaults to 'text/plain'.
    """
    # Get a reference to the bucket
    bucket = CS.bucket(bucket_name)

    # Create a blob object for the file
    blob: storage.Blob = bucket.blob(model_name)

    # Upload the file contents to the blob
    blob.upload_from_string(
        data=model_content,
        content_type=content_type,
    )

    print(f'Model {model_name} uploaded to {bucket_name}.')


def model_save_to_storage(
    CS: storage.Client,
    bucket_name: str,
    model: Pipeline,
    model_name: str = 'nar-rayya',
    content_type: str = 'text/plain',
) -> None:
    """
    Saves a machine learning model to Google Cloud Storage.

    Args:
        CS (google.cloud.storage.client.Client): A Google Cloud Storage client object.
        bucket_name (str): The name of the bucket to save the model to.
        model (sklearn.pipeline.Pipeline): The machine learning model to save.
        model_name (str, optional): The name to give the saved model. Defaults to 'nar-rayya'.
        content_type (str, optional): The content type of the saved model. Defaults to 'text/plain'.

    Returns:
        None
    """
    # https://stackoverflow.com/questions/56880703/read-model-as-bytes-without-saving-in-location-in-python
    # https://stackoverflow.com/questions/51921142/how-to-load-a-model-saved-in-joblib-file-from-google-cloud-storage-bucket
    bytes_container = BytesIO()
    joblib.dump(model, bytes_container)
    bytes_container.seek(0)  # update to enable reading

    _storage_write_bytes_file_to_bucket(
        CS=CS,
        bucket_name=bucket_name,
        model_content=bytes_container.read(),
        model_name=model_name,
        content_type=content_type,
    )


def query_to_pandas_dataframe(
    query: str,
    BQ: bigquery.Client
) -> pd.DataFrame:
    """
    This function takes a SQL query and a BigQuery client object as input, and
    returns the result of the query as a pandas DataFrame.

    Args:
        query (str): The SQL query to execute.
        BQ (bigquery.Client): The BigQuery client object to use for executing the query.

    Returns:
        pd.DataFrame: The result of the query as a pandas DataFrame.
    """
    return BQ.query(query).to_dataframe()
