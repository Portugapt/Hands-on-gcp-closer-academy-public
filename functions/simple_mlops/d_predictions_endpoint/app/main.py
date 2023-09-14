import json
import os
import traceback
import uuid

import flask
import joblib
import pandas as pd
from flask import abort, jsonify, make_response
from google.cloud import bigquery, storage
from sklearn.pipeline import Pipeline

try:
    from funcs import gcp_apis, models
except ImportError:
    from d_predictions_endpoint.app.funcs import (
        gcp_apis,
        models,
    )

# Load the pipeline from the pickle file
pipeline: Pipeline | None = None

################
# 1. Clients ###
################


def load_clients(
    gcp_project_id: str
) -> models.GCPClients:
    """Load the GCP clients.

    Args:
        gcp_project_id (str): The GCP project ID.

    Returns:
        GCPClients: A tuple of GCP clients.
            With the following attributes:
                storage_client: A storage client.
                bigquery_client: A bigquery client.
    """

    storage_client = storage.Client(project=gcp_project_id)
    bigquery_client = bigquery.Client(project=gcp_project_id)

    return models.GCPClients(
        storage_client=storage_client,
        bigquery_client=bigquery_client
    )


def _env_vars() -> models.EnvVars:
    """Load the environment variables.

    This function loads the environment variables required for the application to run. It returns a tuple of environment variables.

    Returns:
        models.EnvVars: A tuple of environment variables.
    """
    # fqn = fully qualified name
    # A table fqn is in the format: project_id.dataset_id.table_id

    return models.EnvVars(
        gcp_project_id=os.getenv("_GCP_PROJECT_ID", 'gcp_project_id'),
        bucket_name=os.getenv("_GCS_BUCKET_NAME_MODELS", 'bucket_name'),
        model_location=os.getenv("_MODEL_LOCATION", 'model_location'),
        predictions_table=f'''{os.getenv("_GCP_PROJECT_ID", "gcp_project_id")}.\
{os.getenv("_BIGQUERY_DATASET_ID", "bq_table_fqn_dst")}.\
{os.getenv("_BIGQUERY_TABLE_ID", "bq_table_fqn_tbl")}''',
    )


def load_model(env_vars: models.EnvVars, gcp_clients: models.GCPClients, model_name='model') -> None:
    """
    Downloads a machine learning model from Google Cloud Storage and loads it into memory using joblib.

    Args:
        env_vars (models.EnvVars): An object containing environment variables required for the function.
        gcp_clients (models.GCPClients): An object containing Google Cloud Platform clients required for the function.

    Returns:
        None
    """
    # Load the pipeline from the pickle file
    global pipeline
    if pipeline is None:
        gcp_apis.transfer_blob_to_temp(
            CS=gcp_clients.storage_client,
            gcs_input_bucket=env_vars.bucket_name,
            file_location=env_vars.model_location,
            model_name=model_name
        )
        pipeline = joblib.load('/tmp/' + model_name)


if os.getenv("_CI_TESTING", 'no') == 'no':
    env_vars = _env_vars()
    gcp_clients = load_clients(gcp_project_id=env_vars.gcp_project_id)
    load_model(env_vars=env_vars, gcp_clients=gcp_clients)


def predict(request: flask.Request) -> flask.Response:
    """
    Endpoint function that receives a POST request with JSON data and returns a prediction as a JSON response.

    Args:
        request (flask.Request): The request object.

    Returns:
        flask.Response: The response object.
    """
    if request.method == 'OPTIONS':
        response = make_response('', 204)
        response.headers.set('Access-Control-Allow-Origin', '*')
        response.headers.set('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.set('Access-Control-Allow-Methods', 'POST')
        return response

    print(request.get_json())
    # Abort if no model is loaded
    if not pipeline:
        print(json.dumps({
            'severity': "WARNING",
            'message': 'No model is running',
            'request': request.get_json()}
        ))
        raise ValueError('No model is running')

    if request.content_type != 'application/json':
        abort(400, "Content-Type must be 'application/json'")
    # Set CORS headers for the preflight request

    try:
        prediction_uuid = str(uuid.uuid1())
        point_json: dict = json.loads(request.data)
        point = pd.DataFrame.from_dict(
            [point_json])  # type: ignore
        prediction = pipeline.predict(point).tolist()[0]  # type: ignore

        # Return the prediction as a JSON response
        response = jsonify({'prediction': prediction,
                            'uuid': prediction_uuid})
        response.headers.set('Access-Control-Allow-Origin', '*')

        gcp_apis.bigquery_insert_json_row(
            BQ=gcp_clients.bigquery_client,  # type: ignore
            table_fqn=env_vars.predictions_table,  # type: ignore
            row=[{k: str(v) for k, v in point_json.items()} | {
                'uuid': prediction_uuid,
                'model_prediction': str(prediction),
                'model_id': 'titanic_basic',
                'model_version': 'allonz-y'}]
        )

        return response
    except Exception as e:
        print(json.dumps({
            'severity': "ERROR",
            'message': 'Request Failed. traceback: {trace}'.format(trace=traceback.print_exc()),
            'request': request.get_json(),
            'error': str(e)}
        ))
        return abort(500, 'Request Failed. traceback: {trace}'.format(trace=traceback.print_exc()))
