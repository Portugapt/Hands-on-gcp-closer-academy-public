from dataclasses import dataclass
from typing import List
from unittest import mock

import pytest
from cloudevents.http import CloudEvent
from google.cloud import bigquery, pubsub, storage

from a_ingest_data.app import main
from a_ingest_data.app.funcs import gcp_apis, models, transform

TEST_ENV = {
    '_GCP_PROJECT_ID': 'test-project',
    '_BIGQUERY_DATASET_ID': 'test-dataset',
    '_BIGQUERY_TABLE_ID': 'test-table',
    'TOPIC_INGESTION_COMPLETE': 'test-topic',
}


@mock.patch.dict('os.environ', TEST_ENV)
def test_env_vars() -> None:
    env_vars = main._env_vars()
    assert env_vars.bq_table_fqn == 'test-project.test-dataset.test-table'


@pytest.fixture
def cloud_event() -> CloudEvent:
    attributes = {
        "specversion": "1.0",
        "id": "1234567890",
        "source": "//storage.googleapis.com/projects/_/buckets/[Bucket Name]",
        "type": "google.cloud.storage.object.v1.finalized",
        "datacontenttype": "application/json",
        "time": "2020-08-08T00:11:44.895529672Z"
    }
    data = {
        "name": "folder/myfile.csv [File path inside the bucket]",
        "bucket": "[Bucket Name]",
        "contentType": "application/json",
        "metageneration": "1",
        "timeCreated": "2020-04-23T07:38:57.230Z",
        "updated": "2020-04-23T07:38:57.230Z"
    }

    return CloudEvent(attributes=attributes, data=data)


@pytest.fixture
def storage_client() -> mock.Mock:
    return mock.Mock(spec=storage.Client)


@pytest.fixture
def bigquery_client() -> mock.Mock:
    return mock.Mock(spec=bigquery.Client)


@pytest.fixture
def publisher() -> mock.Mock:
    return mock.Mock(spec=pubsub.PublisherClient)


@pytest.fixture
def gcp_clients(storage_client, bigquery_client, publisher) -> models.GCPClients:
    return models.GCPClients(
        storage_client=storage_client,
        bigquery_client=bigquery_client,
        publisher=publisher
    )


def test_gcp_clients(
    storage_client: mock.Mock,
    bigquery_client: mock.Mock,
    publisher: mock.Mock,
    gcp_clients: models.GCPClients
) -> None:
    assert gcp_clients.storage_client == storage_client
    assert gcp_clients.bigquery_client == bigquery_client
    assert gcp_clients.publisher == publisher


@pytest.fixture
def env_vars() -> models.EnvVars:
    return models.EnvVars(
        gcp_project_id='test_project',
        bq_table_fqn='test_project.test_dataset.test_table',
        topic_ingestion_complete='test_topic'
    )


@dataclass
class Datapoint:
    col1: str
    col2: str

    def to_dict(self) -> dict:
        return {
            'col1': self.col1,
            'col2': self.col2
        }


@pytest.fixture
def datapoint_in_class() -> List[Datapoint]:
    return [
        Datapoint(col1='value1', col2='value2'),
        Datapoint(col1='value3', col2='value4')
    ]


@pytest.fixture
def datapoints() -> list:
    return [
        {'col1': 'value1', 'col2': 'value2'},
        {'col1': 'value3', 'col2': 'value4'}
    ]


@mock.patch.dict('os.environ', {'_CI_TESTING': 'no'})
def test_main(
    cloud_event: mock.Mock,
    storage_client: mock.Mock,
    bigquery_client: mock.Mock,
    publisher: mock.Mock,
    gcp_clients: models.GCPClients,
    env_vars: models.EnvVars,
    datapoints: list,
    datapoint_in_class: List[Datapoint],
) -> None:
    # Mock the necessary functions
    with mock.patch.object(gcp_apis, 'storage_download_blob_as_string') as mock_download_blob_as_string, \
            mock.patch.object(transform, 'split_lines', return_value=datapoints), \
            mock.patch.object(gcp_apis, 'bigquery_insert_json_row'), \
            mock.patch.object(gcp_apis, 'pubsub_publish_message') as mock_publish_message, \
            mock.patch.object(main, 'load_clients', return_value=gcp_clients), \
            mock.patch.object(transform, 'titanic_transform', return_value=datapoint_in_class), \
            mock.patch.object(main, '_env_vars', return_value=env_vars):

        # Set the mock return values
        mock_download_blob_as_string.return_value = 'col1,col2\nvalue1,value2\nvalue3,value4\n'
        gcp_apis.bigquery_insert_json_row.return_value = None

        # Call the function
        main.main(cloud_event)

        # Assert that the necessary functions were called with the correct arguments
        mock_download_blob_as_string.assert_called_once_with(
            CS=storage_client,
            bucket_name=cloud_event.get_data()['bucket'],
            file_path=cloud_event.get_data()['name']
        )
        transform.split_lines.assert_called_once_with(
            content='col1,col2\nvalue1,value2\nvalue3,value4\n'
        )
        gcp_apis.bigquery_insert_json_row.assert_has_calls([
            mock.call(
                BQ=bigquery_client,
                table_fqn=env_vars.bq_table_fqn,
                row=[datapoints[0]]
            ),
            mock.call(
                BQ=bigquery_client,
                table_fqn=env_vars.bq_table_fqn,
                row=[datapoints[1]]
            )
        ])
        mock_publish_message.assert_called_once_with(
            PS=publisher,
            project_id=env_vars.gcp_project_id,
            topic_id=env_vars.topic_ingestion_complete,
            message=f"I finished ingesting the file {cloud_event.get_data()['name']}!!",
            attributes={}
        )
