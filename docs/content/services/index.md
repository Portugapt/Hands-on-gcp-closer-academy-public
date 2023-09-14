# Services

- [Services](#services)
	- [Google Cloud Storage](#google-cloud-storage)
	- [Cloud Functions](#cloud-functions)
	- [BigQuery](#bigquery)
	- [Pub/Sub (Cloud Pub/Sub)](#pubsub-cloud-pubsub)
	- [Comparison with other providers](#comparison-with-other-providers)

In the world of cloud computing, various cloud service providers offer a wide range of services to cater to different business needs. In this document, we'll introduce and compare some essential services offered by Google Cloud Platform (GCP), along with their counterparts in Amazon Web Services (AWS) and Microsoft Azure.

## Google Cloud Storage

**Google Cloud Storage (GCS)** is a scalable, fully-managed, and highly available object storage service provided by Google Cloud Platform. It allows users to store, access, and manage data across multiple storage classes, catering to various use cases like backup, archival, and content delivery. GCS ensures data durability and offers seamless integration with other Google Cloud services.

**Alternative Services:**

- AWS: Amazon S3 (Simple Storage Service)
- Azure: Azure Blob Storage

## Cloud Functions

**Cloud Functions** is Google Cloud's serverless compute service. It enables you to run event-driven code without managing servers. You can trigger functions in response to various events, such as HTTP requests, changes in Cloud Storage, or Pub/Sub messages.

**Alternative Services:**

- AWS: AWS Lambda
- Azure: Azure Functions

## BigQuery

**BigQuery** is a fully-managed, serverless, petabyte-scale data warehouse by Google Cloud Platform. It enables super-fast SQL queries using the processing power of Google's infrastructure, allowing users to analyze large datasets in real-time. BigQuery is designed for scalability, ease of use, and integration with other Google Cloud services.

**Alternative Services:**

- AWS: Amazon Redshift
- Azure: Azure Synapse Analytics (formerly SQL Data Warehouse)

## Pub/Sub (Cloud Pub/Sub)

**Pub/Sub** stands for "publish/subscribe" and is Google Cloud's messaging service. It allows you to build event-driven systems by decoupling the senders and receivers of messages. It can handle real-time data streaming, event notifications, and asynchronous communication.

**Alternative Services:**

- AWS: Amazon SNS (Simple Notification Service) and Amazon SQS (Simple Queue Service)
- Azure: Azure Service Bus and Azure Event Hubs

## Comparison with other providers

These cloud services provide the fundamental building blocks for modern cloud-based applications, and each cloud provider offers its own unique features and integrations to meet specific business needs.


| Service         | Google Cloud Platform | AWS      | Azure             |
|-----------------|-----------------------|----------|-------------------|
| GCS             | Object storage        | S3       | Blob Storage      |
| Cloud Functions | Serverless computing  | Lambda   | Functions         |
| BigQuery        | Cloud data warehouse  | Redshift | Synapse Analytics |
| Cloud Pub/Sub   | Messaging             | SNS/SQS      | Event Hubs        |
