
import json
from typing import Any, Dict, Sequence

from google.cloud import bigquery, storage


def transfer_blob_to_temp(
    CS: storage.Client,
    gcs_input_bucket: str,
    file_location: str,
    model_name: str = 'model'
) -> None:
    """
    Downloads a blob from a Google Cloud Storage bucket as bytes.

    Args:
        CS (storage.Client): A Google Cloud Storage client object.
        gcs_input_bucket (str): The name of the Google Cloud Storage bucket.
        file_location (str): The location of the blob in the bucket.

    Returns:
        bytes: The contents of the blob as bytes.

    Raises:
        ValueError: If the specified blob does not exist in the bucket.
    """

    # Getting the bucket
    bucket = CS.bucket(gcs_input_bucket)

    # Getting the blob
    blob = bucket.blob(file_location)

    if blob.exists():
        # Downloading the blob
        blob.download_to_filename('/tmp/' + model_name)
    else:
        raise ValueError(f'Blob {file_location} does not exist.')


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
