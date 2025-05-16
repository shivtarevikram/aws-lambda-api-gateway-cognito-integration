# aws-lambda-api-gateway-cognito-integration

## Objective

Create an API based on AWS services that can create a VPC with multiple subnets and store the results. Data of created resources should be accessible from the API. Code should be written in Python. API should be protected with authentication layer and authorization should be open to all authenticated users.

## Overview

This project implements a secure, serverless APIs that can create VPC resources, stores results in DynamoDB and fetches data from DynamoDB table. It has **AWS Lambda** function which is built using Python to create VPC resources, store results in **AWS DynamoDB** and fetches data. APIs are protected using **Amazon Cognito** authorizer. APIs are accesible only to Cognito authenticated users and authorization is open to all authenticated users.

## Features

- Create a VPC and multiple subnets using APIs.
- AWS Lambda function written in Python 3.13 runtime
- AWS API gateway is secured using Amazon Cognito using token based authentication which gets expired in 60 minutes
- AWS APIs are acessible to all authenticated users
- APIs stores and retrieves created VPC resource data
- No manual VPC resources provisioning

## Technologies Used

- AWS Lambda
- AWS API Gateway
- AWS Cognito
- AWS DynamoDB (for resource data storage)
- Boto3 (AWS SDK for Python)
- IAM Role (for providing necessary permissions to provision resources)

## Prerequisites

- AWS account with permissions to manage VPC, Lambda, API Gateway, DynamoDB and Cognito
- AWS IAM role with appropriate IAM permissions
- AWS Lambda function with Python 3.10 or later (AWS is ending support for Python 3.9 in Lambda on November 3, 2025.)

## Setup Instructions

### 1. Clone the Repository
Clone the repository to your machine for Lambda deployment.

### 2. Deploy Lambda Function
- Create the Lambda function and upload lambda_function.py and functions.py files.
- Lambda should have permissions to DynamoDB (for storing results), VPC (for creating VPC and subnets) and CloudWatch (for logs: attach AWS managed policy AWSLambdaBasicExecutionRole).

### 3. Set Up Amazon Cognito
- Create a Cognito User Pool
- Add an App Client (Dont forget to select Implicit Grant option in OAuth 2.0 grant types)

### 4. Configure API Gateway
- Create a new REST API
- Add a resource and POST method for creating VPC resources and storing data in DynamoDB table (e.g., POST /createVPCResources)
- Add a resource and GET method for fetching data from DynamoDB table (e.g., GET /getVPCResources)
- Integrate these APIs with the Lambda function
- Create Cognito authorizer with the Cognito User Pool and attach it to the method requests of both APIs
- To create VPC resources, invoke API with querystring (?op=createVPCResources) and JSON payload provided in vpc_creation_payload.json file along with Authorization token passed in headers.
- To fetch VPC resources, invoke API with querystring (?op=getVPCInfo) and passing Authorization token in headers.

## Authentication
- APIs are secured using Amazon Cognito.
- Only users with valid tokens can access the endpoint.
- Tokens must be passed in the Authorization header as: Authorization: <your-token>

## Security Notes
- No hardcoded secrets are used.
- All access is authenticated via Cognito.
- Lambda functions run with least-privilege IAM roles.
