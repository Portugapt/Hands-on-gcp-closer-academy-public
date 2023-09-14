
# Create Resources (Tables/Buckets/Topics) within GCP

## Buckets (UI)

> ###  What is Google Cloud Storage (GCS)?
>
> Google Cloud Storage (GCS) is a scalable, fully-managed, and highly available object storage service provided by Google Cloud Platform. It allows users to store, access, and manage data across multiple storage classes, catering to various use cases like backup, archival, and content delivery. GCS ensures data durability and offers seamless integration with other Google Cloud services.

1. Search for the Cloud Storage in the Search bar.

    ![img-buckets-1](https://i.imgur.com/voKVC6X.png)

2. In the Cloud Storage UI, you'll notice there are no buckets created yet. To create one, click the `CREATE` button.

    ![img-buckets-2](https://i.imgur.com/kYTszb3.png)

3. Configurate your bucket

    ![img-buckets-3-1](https://i.imgur.com/J3daANw.png)

    1. Name your bucket and click Continue.
    2. Change the storage class from Multi-region to Region. Set the location to europe-west3, as shown in the image, and click Continue.
    3. Keep the remaining settings as they are.
    4. Click create.

    Your configuration should look like this:

    ![img-buckets-4](https://i.imgur.com/vCD4BsS.png)

    If this popup appears, leave the settings as they are.

    ![img-buckets-pupup1](https://i.imgur.com/nty5chF.png)


And now you have your bucket!

![img-buckets-created](https://i.imgur.com/ZXLrCRL.png)

Alternatively, you can create a bucket using [Python](https://cloud.google.com/storage/docs/creating-buckets#storage-create-bucket-python), other Client Libraries, or even advanced Infrastructure-as-Code tools like [Terraform](https://cloud.google.com/storage/docs/creating-buckets#storage-create-bucket-terraform) or [Pulumi](https://www.pulumi.com/registry/packages/gcp/api-docs/storage/bucket/).


## Bigquery Data Sets and Tables (UI)


> ### What is Bigquery?
>
> BigQuery is a fully-managed, serverless, petabyte-scale data warehouse by Google Cloud Platform. It enables super-fast SQL queries using the processing power of Google's infrastructure, allowing users to analyze large datasets in real-time. BigQuery is designed for scalability, ease of use, and integration with other Google Cloud services.


Tables are always associated with a `data set`. First, let's create a `data set`.

1. Go to BigQuery:

   ![img-bq-1](https://i.imgur.com/Qvhqno3.png)

2. Click the bullet points icon next to the project name:

   ![img-bq-2](https://i.imgur.com/bHct9F7.png)

3. Name your data set, change the region, and click `CREATE DATA SET`:

   ![img-bq-3](https://i.imgur.com/47HuJ0A.png)

    Congratulations! You have a `data set`!

    Now, let's create a table:

4. Click the bullets icon next to your data set, and click *Create Table*:

   ![img-bq-4](https://i.imgur.com/TKcNkJX.png)

5. Configure your table settings:

   ![img-bq-5](https://i.imgur.com/jdLc4oo.png)

    Alternatively, you can define the schema using `JSON`:

    ![img-bq-6](https://i.imgur.com/UcDK3uC.png)

And now you have a table too!

Remember the location of the <u>**Table ID**</u>; you might need it later:

![img-bq-7](https://i.imgur.com/VPfsOJQ.png)

Learn more about tables in the [documentation](https://cloud.google.com/bigquery/docs/tables).

You can also create Tables with Infrastructure-As-Code tools. Here are the examples for [Terraform](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table) and for the several [Clients for Pulumi](https://www.pulumi.com/registry/packages/gcp/api-docs/bigquery/table/)

### JSON Schema

> Why should you use JSON schemas when possible?
>
> 1. Structure and consistency: JSON schemas define the structure of your data, ensuring consistency across all records in the table. This helps maintain data integrity and makes it easier to query and analyze the data.
>
> 2. Validation: By specifying a schema, you can enforce data validation rules, such as data types and required fields, ensuring that only valid data is inserted into the table. This can prevent issues caused by incorrect or incomplete data.
>
> 3. Readability: JSON schemas provide a clear and human-readable description of the table's structure, making it easier for team members to understand the data and its organization
>
> 4. Interoperability: JSON schemas are a standardized format, which makes it simpler to share and exchange table structures across teams and different systems. This is particularly useful when integrating with other tools or platforms that support JSON schema.
>
> 5. Easier data import: When importing data from files (e.g., CSV or JSON) into BigQuery, providing a JSON schema allows BigQuery to map the file's data correctly to the table's columns, preventing import errors and ensuring data consistency.

Here's an example of a JSON schema:

```json
[
    {
        "name": "my_required_text_field",
        "type": "STRING",
        "mode": "REQUIRED",
        "description": "A text field"
    },
    {
        "name": "my_required_integer_field",
        "type": "INTEGER",
        "mode": "NULLABLE",
        "description": "An integer field"
    },
    {
        "name": "my_nullable_boolean_field",
        "type": "BOOLEAN",
        "mode": "NULLABLE",
        "description": "A boolean field"
    }
]
```

You can also find it in the folder `./infrastructure/bigquery/example_schema.json`.

You can fiend more about how to define JSON schemas in the [Google Documentation](https://cloud.google.com/bigquery/docs/schemas#specifying_a_json_schema_file).

-----
## Pub/Sub Topics (UI)

> #### What is the Publisher-Subscriber pattern?
>
>       The publisher-subscriber (pub-sub) messaging pattern is a communication paradigm where messages are sent by publishers to multiple subscribers, without requiring direct connections between them. Publishers broadcast messages to topics, and subscribers listen to topics they are interested in. This pattern provides a decoupled architecture, allowing for scalability, flexibility, and fault tolerance. Subscribers receive messages asynchronously, enabling them to process events independently, without blocking or waiting for other subscribers. The pub-sub pattern is widely used in distributed systems, event-driven architectures, and messaging applications.
>
> #### What is Google Pub/Sub?
>
>       Google Pub/Sub is a real-time messaging service based on the publisher-subscriber pattern, designed for Google Cloud Platform. It enables reliable, scalable, and asynchronous event-driven communication between microservices, applications, and data streams, promoting decoupled and flexible architectures.

1. Search for *Topics* in the search bar.
2. Click in **CREATE TOPIC**.

    ![img-ps-1](https://i.imgur.com/iy3OUEr.png)

3. Define your Topic ID and click **CREATE**

    ![img-ps-2](https://i.imgur.com/vzSAAnv.png)

    In this case, our Topic ID is `ingestion_complete`.

    Remember where to find your Topic IDs, it will be useful when instrumenting the python scripts.

4. We have a new topic!

   ![img-ps-3](https://i.imgur.com/UMjA8xS.png)

   It automatically creates a subscription, but lets ignore that for now.

5. If you go back to the Topics page, it should look like this

    ![img-ps-4](https://i.imgur.com/JlcQTuU.png)

Like any other resource, we can also create Topics and Subscriptions with IaC.

Follow these links for examples for [Terraform](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/pubsub_subscription) and [Pulumi](https://www.pulumi.com/registry/packages/gcp/api-docs/pubsub/subscription/).

## Deploy Cloud Functions (gcloud)

In the exercises we will deploy Cloud Functions from a Zip file. For this, we need a bucket specifically for storing the zipped code of the functions. [Find more information on GCP documentation](https://cloud.google.com/functions/docs/deploy#from-cloud-storage), and follow the example in [how to create a bucket](#buckets-ui) to create a bucket for the zipped files.

1. Activate the Cloud Shell

    ![img-cf-d-1](https://i.imgur.com/B5CFhbH.png)

    After a while, you should have a command line in the bottom of your browser. Confirm that you have an active project (green rectangle). If not, contact us.

    ![img-cf-d-2](https://i.imgur.com/RQiseeT.png)

2. Execute the following command:

    ```bash
    gcloud functions deploy [YOUR_FUNCTION_NAME] \
        --region=europe-west3 \
        --runtime=python39 \
        --source=gs://[ZIPPED_FUNCTIONS_BUCKET]/[ZIP_NAME] \
        --entry-point=main \
        TRIGGER_FLAGS
    ```


    `--region`: Deployment Region.
    - [List of Regions](https://cloud.google.com/functions/docs/locations)

    `--runtime`: The execution environment.
    - [Available environments](https://cloud.google.com/functions/docs/concepts/execution-environment) (We will use python39)

    `--source`: Source code of the function.
    - There are several ways to access the source code. We will use [Deploy from Cloud Storage](https://cloud.google.com/functions/docs/deploy#from-cloud-storage). But you can deploy from a source repository or directly from a local machine (your PC).

    `--entry-point`: The *function/code* executed when the **Cloud Function** runs.
    - Learn more here for [event-driven functions](https://cloud.google.com/functions/docs/writing/write-event-driven-functions#background-functions) and for [http functions](https://cloud.google.com/functions/docs/writing/write-http-functions#implementation).

    `TRIGGER_FLAGS`: The trigger type of the Cloud Function.
    - See more in the [table here](https://cloud.google.com/functions/docs/deploy#basics).
    - In our case, we will use three trigger types for the three cloud functions. `--trigger-bucket`, `--trigger-topic` and `--trigger-http`.

    If this shows up:

    ![img-cf-d-3](https://i.imgur.com/eHgr8me.png)

    Type `y`

3. Check the status of your deployment.

    Search for Cloud Build

    ![img-cb-1](https://i.imgur.com/As8xw0T.png)

    And check if you are in Region europe-west3. Something similar to this should show up:

    ![img-cb-2](https://i.imgur.com/X93WnsX.png)

    If the cloud function was deployed with success, you'll get a green check

    ![img-cb-3](https://i.imgur.com/UG8R4wq.png)

    Go to the Cloud Functions UI, and check that your function was deployed with success.

    ![img-cf-d-5](https://i.imgur.com/WysoDXP.png)

    You can click the function name and check it's properties, configurations and even source code deployed.

    For example, we can check if the trigger of a cloud function in the `Trigger` page.

    ![img-cf-d-6](https://i.imgur.com/CcbZCDu.png)

    If your deployment didn't work, let us know and we'll help you.
