import json
import os

import functions_framework
from cloudevents.http import CloudEvent

try:
    from funcs import common, gcp_apis, models, train_models
except ImportError:
    from c_train_model.app.funcs import (
        common,
        gcp_apis,
        models,
        train_models,
    )

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

    storage_client = 'Create a storage client here, with the correct project ID argument'
    bigquery_client = 'Create a bigquery client here, with the correct project ID argument'

    return models.GCPClients(
        storage_client=storage_client,
        bigquery_client=bigquery_client
    )

##############################
# 2. Environment variables ###
##############################


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
        topic_training_complete=os.getenv(
            "_TOPIC_TRAINING_COMPLETE", 'topic_training_complete'),
    )


if os.getenv("_CI_TESTING", 'no') == 'no':
    env_vars = _env_vars()
    gcp_clients = load_clients(gcp_project_id=env_vars.gcp_project_id)


@functions_framework.cloud_event
def main(cloud_event: CloudEvent) -> None:
    """Entrypoint of the cloud function."""
    print(cloud_event)
    if not hasattr(main, 'env_vars'):
        env_vars = _env_vars()

    if not hasattr(main, 'gcp_clients'):
        gcp_clients = load_clients(
            gcp_project_id=env_vars.gcp_project_id)  # type: ignore

    event_message: dict = cloud_event.get_data()  # type: ignore

    data = json.loads(
        common.decode_base64_to_string(
            event_message['message']['data'])
    )
    print(data)

    # Train the model
    if event_message['message']['attributes']['train_model'] == 'True':

        path = common.get_path_to_file()

        ########################################################
        # 3. Create a query that retrieves the training data ###
        ########################################################
        query = common.query_train_data(
            table_fqn='??'
            query_path=path
        )
        df = gcp_apis.query_to_pandas_dataframe(
            query=query,
            BQ=gcp_clients.bigquery_client,  # type: ignore
        )

        pipeline = train_models.titanic_train(
            df=df,
        )

        #######################################################
        # 4. Correct the arguments in model_save_to_storage ###
        #######################################################

        gcp_apis.model_save_to_storage(
            CS='??',
            model='??',
            bucket_name='??'
        )
