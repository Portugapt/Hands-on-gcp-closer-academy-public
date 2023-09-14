from pathlib import Path
from unittest import mock

import pandas as pd
import pytest
from cloudevents.http import CloudEvent
from google.cloud import bigquery, storage

from c_train_model.app import main
from c_train_model.app.funcs import models


@pytest.fixture
def cloud_event():
    attributes = {
        'specversion': '1.0',
        'id': '8609886974320393',
        'source': '//pubsub.googleapis.com/projects/closeracademy-handson/topics/your_name_in_lowercase-update-facts-complete',
        'type': 'google.cloud.pubsub.topic.v1.messagePublished',
        'datacontenttype': 'application/json',
        'time': '2023-09-13T16:38:56.559Z'
    }
    data = {
        'message': {
            'attributes': {
                'dataset': 'titanic',
                'train_model': 'True'
            },
            'data': 'eyJtZXNzYWdlIjogIkkgZmluaXNoZWQgcGFzc2luZyB0aGUgc3RhZ2luZyBkYXRhIHRvIGZhY3RzIiwgInRyYWluaW5nX2RhdGFfdGFibGUiOiAiY2xvc2VyYWNhZGVteS1oYW5kc29uLmptX3Rlc3RfdG9fZGVsZXRlLmptX3Rlc3QtZGVsZXRlLXRpdGFuaWNfZmFjdHMifQ==',
            'messageId': '8609886974320393',
            'message_id': '8609886974320393',
            'publishTime': '2023-09-13T16:38:56.559Z',
            'publish_time': '2023-09-13T16:38:56.559Z'},
        'subscription': 'projects/closeracademy-handson/subscriptions/eventarc-europe-west3-jm-test-train-model-571723-sub-799'
    }
    return CloudEvent(attributes=attributes, data=data)


@pytest.fixture
def storage_client() -> mock.Mock:
    return mock.Mock(spec=storage.Client)


@pytest.fixture
def bigquery_client() -> mock.Mock:
    return mock.Mock(spec=bigquery.Client)


@pytest.fixture
def env_vars():
    return main._env_vars()


@pytest.fixture
def gcp_clients(storage_client, bigquery_client) -> models.GCPClients:
    return models.GCPClients(
        bigquery_client=bigquery_client,
        storage_client=storage_client
    )


def test_load_clients(gcp_clients):
    assert isinstance(gcp_clients.storage_client, storage.Client)
    assert isinstance(gcp_clients.bigquery_client, bigquery.Client)


def test_env_vars(env_vars):
    assert isinstance(env_vars.gcp_project_id, str)
    assert isinstance(env_vars.bucket_name, str)
    assert isinstance(env_vars.topic_training_complete, str)


@pytest.fixture
def env_vars_filled():
    return models.EnvVars(
        gcp_project_id='test_project',
        bucket_name='its_a_bucket',
        topic_training_complete='test_topic',
    )


@pytest.fixture
def simple_pandas_dataframe() -> pd.DataFrame:
    return pd.DataFrame({
        'Survived': [True, False, True, False],
        'PassengerId': [1, 2, 3, 4],
        'Name': ['John Doe', 'Jane Doe', 'Bob Smith', 'Alice Smith'],
        'Sex': ['male', 'female', 'male', 'female'],
        'Pclass': [1, 2, 3, 1],
        'Age': [30, 25, 40, 35],
        'SibSp': [1, 0, 1, 0],
        'Parch': [0, 1, 0, 1],
        'Ticket': ['1234', '5678', '9101', '1121'],
        'Fare': [10.0, 20.0, 30.0, 40.0],
        'Cabin': ['A1', 'B2', 'C3', 'D4'],
        'Embarked': ['S', 'C', 'S', 'C']
    })


@mock.patch('c_train_model.app.main._env_vars')
@mock.patch('c_train_model.app.main.load_clients')
@mock.patch('c_train_model.app.main.gcp_apis.query_to_pandas_dataframe')
@mock.patch('c_train_model.app.main.gcp_apis.model_save_to_storage')
@mock.patch('c_train_model.app.main.common.query_train_data')
def test_main(
    mock_query_train_data: mock.Mock,
    mock_model_save_to_storage: mock.Mock,
    mock_query_to_pandas_dataframe: mock.Mock,
    mock_load_clients: mock.Mock,
    mock_env_vars: mock.Mock,
    cloud_event: CloudEvent,
    env_vars_filled: models.EnvVars,
    gcp_clients: models.GCPClients,
    simple_pandas_dataframe: pd.DataFrame,
) -> None:

    mock_query_train_data.return_value = 'SELECT * FROM some_table'
    mock_load_clients.return_value = gcp_clients
    mock_query_to_pandas_dataframe.return_value = simple_pandas_dataframe
    mock_env_vars.return_value = env_vars_filled
    main.main(cloud_event)

    mock_query_train_data.assert_called_once_with(
        table_fqn='closeracademy-handson.jm_test_to_delete.jm_test-delete-titanic_facts',
        query_path=Path('./resources/select_train_data.sql')
    )

    mock_query_to_pandas_dataframe.assert_called_once_with(
        query=main.common.query_train_data(
            table_fqn='closeracademy-handson.jm_test_to_delete.jm_test-delete-titanic_facts',
            query_path=Path('./resources/select_train_data.sql')
        ),
        BQ=gcp_clients.bigquery_client,
    )

    mock_model_save_to_storage.assert_called_once_with(
        CS=gcp_clients.storage_client,
        model=mock.ANY,
        bucket_name=env_vars_filled.bucket_name,
    )
