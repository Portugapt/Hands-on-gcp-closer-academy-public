import pathlib
from unittest import mock

import pytest
from functions_framework import create_app
from google.cloud import bigquery, storage

from d_predictions_endpoint.app import main  # noqa
from d_predictions_endpoint.app.funcs import gcp_apis  # noqa


def _relative_path() -> pathlib.Path:
    """Returns the relative path of the main.py file."""
    return pathlib.Path(__file__).parent


TEST_FUNCTIONS_DIR = _relative_path() / ".."


@pytest.fixture
def storage_client() -> mock.Mock:
    return mock.Mock(spec=storage.Client)


@pytest.fixture
def storage_bucket() -> mock.Mock:
    return mock.Mock(spec=storage.Bucket)


@pytest.fixture
def storage_blob() -> mock.Mock:
    return mock.Mock(spec=storage.Blob)


@pytest.fixture
def bigquery_client() -> mock.Mock:
    return mock.Mock(spec=bigquery.Client)


@pytest.fixture
def tempfile_payload(tmpdir):
    return {"filename": str(tmpdir / "filename.txt"), "value": "some-value"}


@pytest.fixture
def model_bytes() -> bytes:
    model_path = _relative_path() / "resources" / "nar-rayya"
    with open(model_path, "rb") as f:
        model_bytes = f.read()
    return model_bytes


@pytest.fixture
def background_json(tempfile_payload):
    return {
        "context": {
            "eventId": "some-eventId",
            "timestamp": "some-timestamp",
            "eventType": "some-eventType",
            "resource": "some-resource",
        },
        "data": tempfile_payload,
    }


@mock.patch.dict('os.environ', {'_CI_TESTING': 'no'})
@mock.patch('google.cloud.bigquery.Client', spec=bigquery.Client)
@mock.patch('google.cloud.storage.Blob', spec=storage.Blob)
@mock.patch('google.cloud.storage.Bucket', spec=storage.Bucket)
@mock.patch('google.cloud.storage.Client', spec=storage.Client)
@mock.patch('d_predictions_endpoint.app.funcs.gcp_apis.transfer_blob_as_bytes')
def test_predict_function_executes(
    mock_transfer_blob_as_bytes,
    mock_storage_client: mock.Mock,
    mock_storage_bucket: mock.Mock,
    mock_storage_blob: mock.Mock,
    mock_bq_client: mock.Mock,
    model_bytes: bytes,
):
    with mock.patch.object(storage.Blob, 'download_as_bytes'):
        mock_storage_client.return_value.bucket.return_value = mock_storage_bucket
        mock_storage_bucket.return_value.blob.return_value = mock_storage_blob
        mock_transfer_blob_as_bytes.return_value = model_bytes

        source = TEST_FUNCTIONS_DIR / "app" / "main.py"
        target = "predict"

        app = create_app(target, source)

        test_client = app.test_client()

        resp = test_client.post(
            "/",
            json={"Age": 2, "SibSp": 3, "Parch": 4,
                  "Fare": 4, "Sex": "male", "Embarked": "C",
                  "Pclass": "3"})
        assert resp.status_code == 200

        assert resp.data == b"success"


# @pytest.fixture
# def client():
#     app = Flask(__name__)
#     app.config['TESTING'] = True

#     with app.test_client() as client:
#         yield client


# def test_predict(client):
#     # Mock the request object
#     request_data = {'input': [1, 2, 3]}
#     request = MagicMock()
#     request.content_type = 'application/json'
#     request.data = json.dumps(request_data).encode('utf-8')

#     # Call the predict function
#     response = predict(request)

#     # Check the response
#     assert response.status_code == 200
#     assert response.mimetype == 'text/plain'
#     assert response.data == b'Hello World!'
