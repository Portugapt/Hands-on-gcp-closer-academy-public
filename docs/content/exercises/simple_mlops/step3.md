# Deploy a Cloud function that trains a model and saves it in GCS

- [Deploy a Cloud function that trains a model and saves it in GCS](#deploy-a-cloud-function-that-trains-a-model-and-saves-it-in-gcs)
  - [Introduction](#introduction)
  - [Tasks](#tasks)
  - [Create the Google Cloud Resources](#create-the-google-cloud-resources)
    - [1. Create the models GCS Bucket](#1-create-the-models-gcs-bucket)
  - [Update the Cloud Function Code](#update-the-cloud-function-code)
  - [Deploy the cloud function](#deploy-the-cloud-function)
  - [Documentation](#documentation)

## Introduction

![img-train_model-architecture](./resources/part_3/model_v2.png)

In this exercise, we will create a Cloud Function called `Train Model`, which will be responsible for training a machine learning model using the data ingested in the previous steps. The function will be triggered by the `ingestion_complete` Pub/Sub topic, ensuring it starts training once new data is available in the BigQuery table. The steps involved in this process are as follows:

1. The `Train Model` Cloud Function is subscribed to the `[yourname]-update-facts-complete` topic, and it will be triggered automatically when a new message is published, indicating that new data has been loaded into the BigQuery table.

2. Upon being triggered, the `train_model` function retrieves the data from the `Titanic Facts` BigQuery table using the appropriate query. This data will be used to train a machine learning model, such as a Scikit-learn Random Forest or Logistic Regression model.

3. After the model is trained using the fetched data, the `Train Model` function saves the trained model to the `[yourname]-models` Google Cloud Storage bucket. You can choose the name for this model, but it should be unique.

This exercise will guide you through the process of developing the `train_model` Cloud Function, which leverages the power of BigQuery, Scikit-learn, and Google Cloud Storage to create, train, and store a machine learning model.

For this you will need these resources:

- The already created *Data Set* in step 1.
- The already created *Bigquery Table* in step 2.
- A Pub/Sub topic named `[yourname]-train_model-complete` where you will publish a success message.
- One GCS Bucket named `[yourname]-models` where you will save the model

The outline of the *Cloud Function* code is available at `./functions/manual_exercises/c_train_model/app`

```text
c_train_model/
├── app/
│   ├── funcs/
│   │   ├── models.py # Models to make typechecking easier.
│   │   ├── gcp_apis.py # Functions to call google services.
│   │   ├── common.py # Common functions (Utils).
|   |   └── train_model.py # Train model functions
│   ├── main.py # Main module and entry point for the Cloud Function
│   └── requirements.txt # Requirements for the function execution.
├── config/
│   └── dev.env.yaml # Environment variables that will ship with the function deployment
└── tests/
    └── test_*.py # Unit tests.
```

## Tasks

- [ ] Create the Google Cloud Resources
- [ ] Update the Cloud Function Code
- [ ] Test the Cloud Function
- [ ] Deploy the Cloud Function

## Create the Google Cloud Resources

Here are the resources necessary to complete the exercise:

You can create the resources with Cloud Shell or in the Console.
***The end result will be the same. When creating a resource, choose either to create it with the cloud shell or the console, but not both.***

For Cloud Shell, set these variables:

```bash
export PROJECT_NAME=$(gcloud config get-value project)
export REGION=europe-west3
export YOURNAME=your_name_in_lowercase
```

![img-cloudshell](https://i.imgur.com/5vmuTn8.png)

### 1. Create the models GCS Bucket

```bash
gsutil mb \
    -c regional \
    -l ${REGION} \
    -p ${PROJECT_NAME} \
    gs://${YOURNAME}-models-c

gsutil label ch -l owner:${YOURNAME} gs://${YOURNAME}-models
gsutil label ch -l project:${PROJECT_NAME} gs://${YOURNAME}-models
gsutil label ch -l purpose:academy gs://${YOURNAME}-models
```

Reference: [gsutil mb](https://cloud.google.com/storage/docs/gsutil/commands/mb), [gsutil label](https://cloud.google.com/storage/docs/gsutil/commands/label)

With the console:

Same as in step 1, but now the bucket name is `[yourname]-models`

## Update the Cloud Function Code

1. Create the client objects: Use the Google Cloud BigQuery API, and Storage API to create respective client objects.

    ```python
    ################
    # 1. Clients ###
    ################
    storage_client = 'Create a storage client here, with the correct project ID argument'
    bigquery_client = 'Create a bigquery client here, with the correct project ID argument'

    return models.GCPClients(
        storage_client=storage_client,
        bigquery_client=bigquery_client,
    )
    ```

2. Set Environment Variables

    In the `c_train_model/config/dev.env.yaml` file, change the environment variables for the correct ones.

    ```python
    ##############################
    # 2. Environment variables ###
    ##############################
    ```

    ```yaml
    _GCP_PROJECT_ID: "The GCP project ID where the resources are located"
    _GCS_BUCKET_NAME_MODELS: "The GCS bucket name where the models will be saved"
    _TOPIC_TRAINING_COMPLETE: "The Pub/Sub topic name where the success message will be published"
    ```

3. Create the SQL Query

    You can find the query to change in the `c_train_model/app/resources/select_train_data.sql` file.

    ```python
    ########################################################
    # 3. Create a query that retrieves the training data ###
    ########################################################
    query = common.query_train_data(
        table_fqn='??'
        query_path=path
    )
    ```

    ```sql
    SELECT 'THIS QUERY IS NOT IMPLEMENTED YET' FROM `{table_source}`
    ```

    **Do not change to \`{table_source}\` section.**

4. Correct the arguments in the `model_save_to_storage` function

    ```python
    gcp_apis.model_save_to_storage(
        CS='??',
        model='??',
        bucket_name='??'
    )
    ```

## Deploy the cloud function

You can check the deployment here in [Cloud Build](https://console.cloud.google.com/cloud-build/builds;region=europe-west3?referrer=search&project=closeracademy-handson)

Reference: [gcloud functions deploy](https://cloud.google.com/sdk/gcloud/reference/functions/deploy)

```bash
FUNCTION_NAME="train_model"
YOURNAME="your_name_in_lowercase"

gcloud beta functions deploy $YOURNAME-$FUNCTION_NAME \
    --gen2 --cpu=1 --memory=512MB \
    --region=europe-west3 \
    --runtime=python311 \
    --source=functions/simple_mlops/c_train_model/app/ \
    --env-vars-file=functions/simple_mlops/c_train_model/config/dev.env.yaml \
    --entry-point=main \
    --trigger-topic=$YOURNAME-update-facts-complete
```

## Documentation

Does not work without the code correct.