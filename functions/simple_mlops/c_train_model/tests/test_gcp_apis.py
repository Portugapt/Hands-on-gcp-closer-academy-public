from unittest import mock

import pandas as pd
import pytest
from google.cloud import storage
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

from c_train_model.app.funcs.gcp_apis import model_save_to_storage
from c_train_model.app.funcs.train_models import titanic_train


@pytest.fixture
def storage_client() -> mock.Mock:
    return mock.Mock(spec=storage.Client)


def blob_fixture() -> mock.Mock:
    return mock.Mock(spec=storage.Blob)


@pytest.fixture
def pipeline_titanic() -> Pipeline:
    df = pd.DataFrame({
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

    return titanic_train(df, classifier=RandomForestClassifier())


@pytest.fixture(scope="module")
def trained_model(iris_data):
    X, y = iris_data
    model = RandomForestClassifier()
    model.fit(X, y)
    return model


@mock.patch("google.cloud.storage.Blob", spec=storage.Blob)
@mock.patch("google.cloud.storage.Bucket", spec=storage.Bucket)
@mock.patch("google.cloud.storage.Client", spec=storage.Client)
def test_model_save_to_storage(
    mock_client: mock.Mock,
    mock_bucket: mock.Mock,
    mock_blob: mock.Mock,
    pipeline_titanic: Pipeline
) -> None:
    bucket_name = "test-bucket"
    model_name = "test-model.joblib"

    mock_client.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    mock_blob.upload_from_string.return_value = None

    model_save_to_storage(mock_client, bucket_name,
                          pipeline_titanic, model_name)
