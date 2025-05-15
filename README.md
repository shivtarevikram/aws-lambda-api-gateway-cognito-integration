# aws-lambda-api-gateway-cognito-integration

## Objective

Create an API based on AWS services that can create a VPC with multiple subnets and store the results. Data of created resources should be accessible from the API. Code should be written in Python. API should be protected with authentication layer and authorization should be open to all authenticated users.

## Overview

This project creates **AWS Lambda** function built using Python to create VPC resources, store results in **AWS DynamoDB**. Also implements a secure, serverless API that fetches an result stored in DyanmoDB table containing VPC ID with subnets details. The API is protected using **Amazon Cognito** authorizer. API is accesible only to Cognito authenticated users and authorization is open to all authenticated users.

## Features

- Create a VPC and multiple subnets by invoking Lambda function
- AWS Lambda function written in Python 3.13 runtime
- AWS API gateway is Secured using Amazon Cognito using token based authentication which gets expired in 60 minutes
- AWS API is acessible to all authenticated users
- Stores and retrieves created VPC resource data

## Technologies Used

- AWS Lambda
- AWS API Gateway
- AWS Cognito
- AWS DynamoDB (for resource data storage)
- Boto3 (AWS SDK for Python)
- IAM Role (for providing necessary permissions to provision resources)

## Prerequisites

- AWS account with permissions to manage VPC, Lambda, API Gateway, and Cognito
- AWS IAM role with appropriate IAM permissions
- AWS Lambda function with Python 3.8 or later

## Setup Instructions

### 1. Clone the Repository
Clone the repository to your machine for Lambda deployment.

### 2. Deploy Lambda Function
You can zip and upload the Lambda function.
zip function.zip lambda_function.py
aws lambda update-function-code --function-name createVpcFunction --zip-file fileb://function.zip
To create VPC resources, invoke lambda function using JSON object provided in event_to_invoke_lambda.json file.

### 3. Configure API Gateway
Create a new REST API

Add a resource and GET method (e.g., GET /getVPCResources)

Integrate with your Lambda function

Add a Cognito authorizer and require it on the method

### 4. Set Up Amazon Cognito
Create a Cognito User Pool

Add an App Client

Use the User Pool as the API Gateway authorizer

Integrate Cognito in API gateway

## Authentication
The API is secured using Amazon Cognito.

Only users with valid tokens can access the endpoint.

Tokens must be passed in the Authorization header as:
Authorization: <your-token>

## Security Notes
No hardcoded secrets are used.

All access is authenticated via Cognito.

Lambda functions run with least-privilege IAM roles.
