from unittest import mock

import pytest
from cloudevents.http import CloudEvent
from google.cloud import bigquery, pubsub

from b_update_facts.app import main
from b_update_facts.app.funcs import common, gcp_apis, models


@pytest.fixture
def cloud_event():
    attributes = {
        'specversion': '1.0',
        'id': '8608612983684497',
        'source': '//pubsub.googleapis.com/projects/closeracademy-handson/topics/your_name_in_lowercase-ingestion-complete',
        'type': 'google.cloud.pubsub.topic.v1.messagePublished',
        'datacontenttype': 'application/json',
        'time': '2023-09-13T15:11:47.233Z'}
    data = {
        'message': {
            'data': 'SSBmaW5pc2hlZCBpbmdlc3RpbmcgdGhlIGZpbGUgdGl0YW5pYy5jc3YhIQ==',
            'messageId': '8608612983684497',
            'message_id': '8608612983684497',
            'publishTime': '2023-09-13T15:11:47.233Z',
            'publish_time': '2023-09-13T15:11:47.233Z'},
        'subscription': 'projects/closeracademy-handson/subscriptions/eventarc-europe-west3-jm-test-update-facts-913468-sub-089'
    }
    return CloudEvent(attributes=attributes, data=data)


@pytest.fixture
def bigquery_client() -> mock.Mock:
    return mock.Mock(spec=bigquery.Client)


@pytest.fixture
def publisher() -> mock.Mock:
    return mock.Mock(spec=pubsub.PublisherClient)


@pytest.fixture
def gcp_clients(publisher, bigquery_client) -> models.GCPClients:
    return models.GCPClients(
        bigquery_client=bigquery_client,
        publisher=publisher
    )


def test_gcp_clients(
    bigquery_client: mock.Mock,
    publisher: mock.Mock,
    gcp_clients: models.GCPClients,
) -> None:
    """
    Test function to check if the GCP clients are correctly initialized.

    Args:
        bigquery_client (mock.Mock): A mock object of the BigQuery client.
        publisher (mock.Mock): A mock object of the Pub/Sub publisher.
        gcp_clients (models.GCPClients): An instance of the GCPClients class.

    Returns:
        None
    """
    assert gcp_clients.bigquery_client == bigquery_client
    assert gcp_clients.publisher == publisher


@pytest.fixture
def env_vars():
    return models.EnvVars(
        gcp_project_id='test_project',
        bq_facts_table_fqn='test_project.test_dataset.test_table',
        bq_staging_table_fqn='test_project.test_dataset.test_table',
        topic_update_facts_complete='test_topic',
    )


def test_main(
    cloud_event: CloudEvent,
    gcp_clients: models.GCPClients,
    env_vars: models.EnvVars,
) -> None:
    """
    Test function for the main function in the update_facts module.

    Args:
        cloud_event (CloudEvent): A CloudEvent object.
        gcp_clients (models.GCPClients): A GCPClients object.
        env_vars (models.EnvVars): An EnvVars object.

    Returns:
        None
    """
    with mock.patch.object(gcp_apis, 'execute_query_result') as mock_execute_query_results, \
            mock.patch.object(gcp_apis, 'pubsub_publish_message') as mock_pubsub_publish_message, \
            mock.patch.object(main, 'load_clients', return_value=gcp_clients), \
            mock.patch.object(main, '_env_vars', return_value=env_vars), \
            mock.patch.object(common, 'load_query', return_value='SELECT * FROM table'):

        # Call the function
        main.main(cloud_event)

        mock_execute_query_results.assert_called_once_with(
            BQ=gcp_clients.bigquery_client,
            query='SELECT * FROM table'
        )

        mock_pubsub_publish_message.assert_called_once_with(
            PS=gcp_clients.publisher,
            project_id=env_vars.gcp_project_id,
            topic_id=env_vars.topic_update_facts_complete,
            message="I finished passing the staging data to facts",
            attributes={
                'train_model': 'True',
                'dataset': 'titanic'
            }
        )
