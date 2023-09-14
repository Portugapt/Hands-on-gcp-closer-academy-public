# Query Staging to Facts

- [Query Staging to Facts](#query-staging-to-facts)
  - [Introduction](#introduction)
  - [Tasks](#tasks)
  - [Create the Google Cloud Resources](#create-the-google-cloud-resources)
    - [1. Create a BigQuery Table](#1-create-a-bigquery-table)
    - [2. Create the pubsub topic for update facts complete](#2-create-the-pubsub-topic-for-update-facts-complete)
  - [Update the Cloud Function Code](#update-the-cloud-function-code)
  - [Deploy the cloud function](#deploy-the-cloud-function)
  - [Documentation](#documentation)

## Introduction

![img-staging-facts-architecture](./resources/part_2/staging_facts_v1.png)

In this exercise, we will create the `Query To Facts` Cloud Function, that will perform the following tasks:

1. Activated by the topic `[yourname]-ingestion-complete`.

2. It will send a query to be executed in BigQuery. This query is already done, and will move the data from the staging table to a facts table.

3. After successfully executing the query, this function will send a message to the topic `[yourname]-update-facts-complete`.

The Cloud Function `Ingest Data` will utilize the BigQuery, and Pub/Sub client libraries for these tasks. Our goal in this exercise is to fix the code for this function to make it function preperly and deploy it to Google Cloud.

The resources needed these tasks are:

- The already created *Data Set* in step 1.
- One Bigquery table, `Titanic Facts`
  - The table schema is at: `./infrastructure/bigquery/facts_titanic_schema.json`
- Two Pub/Sub topics, the one already created, and one named `[yourname]-update-facts-complete`, to where the function will send a message once complete.

The outline of the *Cloud Function* code is available at `functions/simple_mlops/2_update_facts/app`.

```text
.
└── b_update_facts/
    ├── app/
    │   ├── funcs/
    │   │   ├── models.py # Models to make typechecking easier.
    │   │   ├── gcp_apis.py # Functions to call google services.
    │   │   └── common.py # Common functions (Utils).
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
export PROJECT_ID=$(gcloud config get-value project)
export PROJECT_NAME=$(gcloud config get-value project)
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
export REGION=europe-west3
export YOURNAME=your_name_in_lowercase
```

![img-cloudshell](https://i.imgur.com/5vmuTn8.png)

### 1. Create a BigQuery Table

With Cloud Shell (Copy-paste):

```bash
bq mk \
    --project_id ${PROJECT_ID} \
    --table \
    --description "Facts table for the Titanic dataset" \
    --label=owner:${YOURNAME} \
    --label=project:${PROJECT_NAME} \
    --label=purpose:academy \
    --label=dataset:titanic \
    ${YOURNAME}_titanic.titanic_facts \
    ./infrastructure/bigquery/facts_titanic_schema.json
```

Reference: [bq mk --table](https://cloud.google.com/bigquery/docs/reference/bq-cli-reference#mk-table)

With the console:

Same as step 1, but now with the schema `facts_titanic_schema.json`

### 2. Create the pubsub topic for update facts complete

With Cloud Shell:

```bash
gcloud pubsub topics create ${YOURNAME}-update-facts-complete \
    --project=${PROJECT_ID} \
    --labels=owner=${YOURNAME},project=${PROJECT_NAME},purpose=academy
```

With the Cloud Console:

Same as before, but now with the name `[yourname]-update-facts-complete`

Now we are ready to move to the cloud function code.

## Update the Cloud Function Code

Here are the steps necessary to complete the exercise:

1. Create the client objects: Use the Google Cloud BigQuery API, and PubSub API to create respective client objects.

    ```python
    ################
    # 1. Clients ###
    ################
    bigquery_client = 'Create a bigquery client here, with the correct project ID argument'
    publisher = 'Create a publisher client here, with the correct project ID argument'

    return models.GCPClients(
        bigquery_client=bigquery_client,
        publisher=publisher
    )
    ```

2. Set Environment Variables

    In the `b_update_facts/config/dev.env.yaml` file, change the environment variables for the correct ones.

    ```python
    ##############################
    # 2. Environment variables ###
    ##############################
    ```

    ```yaml
    _GCP_PROJECT_ID: "The GCP project ID where the resources are located"
    _BIGQUERY_DATASET_ID: "The BigQuery dataset ID you created"
    _BIGQUERY_FACTS_TABLE_ID: "The BigQuery staging table ID"
    _BIGQUERY_STAGING_TABLE_ID: "The BigQuery facts table ID where the data will be moved towards"
    _TOPIC_UPDATE_FACTS_COMPLETE: "The Pub/Sub topic ID where you will send a message once the data is ingested"
    ```

3. Send the correct arguments to the `load_query` function.

    ```python
    #################################################
    # 3. Send the correct arguments to load_query ###
    #################################################

    path = Path('./resources/staging_to_facts.sql')

    query = common.load_query(
        table_facts='??',
        table_raw='??',
        query_path=path,
    )
    ```

4. Send the correct arguments to `execute_query_result`.

    ```python
    #################################################
    # 4. Send the correct arguments execute query ###
    #################################################

    _ = gcp_apis.execute_query_result(
        BQ='??',
        query='??'
    )
    ```

5. Publish Message: Correct the arguments in the `pubsub_publish_message` function, to publish a message.

    ```python
    #########################################################
    # 5. Correct the arguments below to publish a message ###
    #########################################################
    gcp_apis.pubsub_publish_message(
        PS='??',
        project_id='??',
        topic_id='??',
        message=json.dumps({
            'message': "I finished passing the staging data to facts",
            'training_data_table': '??'}),
        attributes={
            'train_model': 'True',
            'dataset': 'titanic'},
    )
    ```

    Hint: you'll have to send to the subscribers which table you added data to.

## Deploy the cloud function

You can check the deployment here in [Cloud Build](https://console.cloud.google.com/cloud-build/builds;region=europe-west3?referrer=search&project=closeracademy-handson)

Reference: [gcloud functions deploy](https://cloud.google.com/sdk/gcloud/reference/functions/deploy)

```bash
FUNCTION_NAME="update-facts"
YOURNAME="your_name_in_lowercase"

gcloud beta functions deploy $YOURNAME-$FUNCTION_NAME \
    --gen2 --cpu=1 --memory=512MB \
    --region=europe-west3 \
    --runtime=python311 \
    --source=functions/simple_mlops/b_update_facts/app/ \
    --env-vars-file=functions/simple_mlops/b_update_facts/config/dev.env.yaml \
    --entry-point=main \
    --trigger-topic=${YOURNAME}-ingestion-complete
```

## Documentation


Does not work without the code correct.