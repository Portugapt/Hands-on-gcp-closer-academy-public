# Serverless

- [Serverless](#serverless)
	- [History](#history)
		- [1. Early Web Hosting and Managed Services](#1-early-web-hosting-and-managed-services)
		- [2. Rise of PaaS (Platform as a Service)](#2-rise-of-paas-platform-as-a-service)
		- [3. Introduction of Amazon AWS Lambda (2014)](#3-introduction-of-amazon-aws-lambda-2014)
		- [4. Google Cloud Functions (2017)](#4-google-cloud-functions-2017)
		- [5. Serverless Frameworks and Ecosystem Growth](#5-serverless-frameworks-and-ecosystem-growth)
		- [6. Azure Functions and Other Cloud Providers](#6-azure-functions-and-other-cloud-providers)
		- [7. Serverless Adoption and Use Cases](#7-serverless-adoption-and-use-cases)
		- [8. Evolving Serverless Features](#8-evolving-serverless-features)
	- [What is Serverless?](#what-is-serverless)
	- [Cloud Functions SDK](#cloud-functions-sdk)

## History

Serverless computing has evolved over the years and has become a popular paradigm for building scalable and cost-effective cloud applications. Below is a brief history of serverless computing and how it led to the creation of AWS Lambda and Google Cloud Functions:

### 1. Early Web Hosting and Managed Services

Before serverless computing became a distinct concept, cloud providers offered various forms of managed services and web hosting solutions. These services allowed developers to deploy applications without worrying about server management but still required them to provision and manage servers manually.

### 2. Rise of PaaS (Platform as a Service)

Platform as a Service (PaaS) offerings, such as Google App Engine and Heroku, started to gain popularity. These platforms abstracted away even more of the infrastructure management tasks, allowing developers to focus solely on writing code and deploying applications.

### 3. Introduction of Amazon AWS Lambda (2014)

In November 2014, AWS Lambda was introduced by Amazon Web Services. AWS Lambda is often considered a pioneering service in the serverless computing space. It allows developers to run code in response to events, such as **HTTP requests, file uploads, database changes, or scheduled events**, without managing servers. AWS Lambda introduced the concept of "functions" where developers could write code in response to specific triggers.

### 4. Google Cloud Functions (2017)

In March 2017, Google Cloud Functions was launched as Google's serverless computing offering. Similar to AWS Lambda, Google Cloud Functions enables developers to **run event-driven functions in response to various triggers** within the Google Cloud ecosystem. This service is tightly integrated with other Google Cloud services like Cloud Storage, Pub/Sub, and BigQuery.

### 5. Serverless Frameworks and Ecosystem Growth

As serverless computing gained popularity, a vibrant ecosystem of serverless frameworks, tools, and libraries emerged. These frameworks, like the Serverless Framework and AWS SAM (Serverless Application Model), aimed to simplify the development and deployment of serverless applications across multiple cloud providers.

### 6. Azure Functions and Other Cloud Providers

Microsoft Azure introduced Azure Functions, its serverless computing offering, which allows developers to build and run event-driven functions in the Azure cloud environment. Other cloud providers, including IBM Cloud, Oracle Cloud, and Alibaba Cloud, also introduced their own serverless offerings, expanding the availability of serverless computing to a wider audience.

### 7. Serverless Adoption and Use Cases

Serverless computing has found adoption across various industries and use cases, including web applications, IoT, real-time data processing, and more. It has become a fundamental part of modern cloud application architecture, offering benefits like auto-scaling, cost optimization, and reduced operational overhead.

### 8. Evolving Serverless Features

Over time, serverless platforms like AWS Lambda and Google Cloud Functions have continued to evolve, introducing new features, language support, and integrations. This evolution has made it easier for developers to build complex and scalable applications while embracing the serverless paradigm.

## What is Serverless?

Serverless computing is a cloud computing model that abstracts away the underlying infrastructure and server management, allowing developers to focus solely on writing and deploying code. In a serverless architecture, developers write functions or small units of code that are executed in response to specific events or triggers, without the need to provision, configure, or manage servers. Here are key characteristics and concepts of serverless computing:

1. **Event-Driven Execution:** Serverless functions are typically triggered by events, such as HTTP requests, database changes, file uploads, timers, or messages from message queues. These events initiate the execution of the function, and the function processes the event data.

2. **Automatic Scaling:** Serverless platforms automatically scale the number of function instances up or down based on the incoming workload. This ensures that functions can handle varying levels of traffic and scale to meet demand without manual intervention.

3. **Stateless and Statelessless:** Serverless functions are designed to be stateless, meaning they don't maintain any persistent state between invocations. Any required state should be stored externally, such as in a database or storage service.

4. **Pay-Per-Use Billing:** With serverless computing, you pay only for the compute resources used during the execution of your functions. There are no upfront costs or charges for idle resources, making it cost-effective for applications with variable workloads.

5. **Short-Lived Execution:** Serverless functions are typically designed to execute quickly, usually completing their tasks in seconds to a few minutes. Long-running processes may be better suited for other computing models.

6. **Managed Services:** Serverless platforms, offered by cloud providers like AWS Lambda, Google Cloud Functions, and Azure Functions, handle server provisioning, maintenance, and scaling. This offloads the operational burden from developers.

7. **Event Sources and Triggers:** Events can come from various sources and triggers, such as HTTP requests (API Gateway), database changes (DynamoDB streams, triggers), file uploads (storage services), messages (message queues like AWS SQS or Pub/Sub), or scheduled events (cron-like triggers).

8. **Language Support:** Serverless platforms typically support multiple programming languages, allowing developers to write functions in their preferred language.

9. **Ephemeral Compute:** Serverless functions are ephemeral, meaning they are created, executed, and then destroyed. This differs from traditional server-based computing, where servers may persist for longer durations.

Serverless computing is well-suited for a wide range of use cases, including web applications, microservices, real-time data processing, IoT applications, and more. It offers benefits like cost savings, scalability, reduced operational complexity, and faster development cycles. However, it's important to consider the statelessness and execution duration limitations when designing serverless applications, as these factors can impact application architecture and design decisions.

## Cloud Functions SDK

Developing Google Cloud Functions (GCF) typically involves writing code in one of the supported programming languages and using the respective Google Cloud SDKs (Software Development Kits) and libraries for that language. The sdk used is the [Google Cloud Functions Framework](https://github.com/GoogleCloudPlatform/functions-framework).

1. **Python:**
      - **Google Cloud Functions Framework for Python:** This is the official library for developing Python-based Google Cloud Functions. It offers a Flask-like interface for building HTTP-triggered functions.

2. **Node.js (JavaScript/TypeScript):**
      - **Google Cloud Functions Framework for Node.js:** This is an official Google library that simplifies the development of Node.js Cloud Functions. It allows you to write functions as Express.js or HTTP functions.
      - **`@google-cloud/functions-framework`:** This is another library provided by Google that enables you to run Node.js functions locally for testing.

3. **Go:**
      - **`github.com/GoogleCloudPlatform/functions-framework-go`:** This community-supported library lets you build Go-based Google Cloud Functions using the Functions Framework.

4. **Java:**
      - **Google Cloud Functions Framework for Java:** This is the official library for Java-based Google Cloud Functions. It provides an easy way to write and deploy Java functions.

5. **.NET (C#):**
      - **Google.Cloud.Functions.Framework:** This is a community-supported library that helps you build Google Cloud Functions using .NET Core and C#.
