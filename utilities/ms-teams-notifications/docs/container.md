# Lambda Container Overview for ms-teams-notifications

This document describes a GitHub Actions workflow designed for deploying the ms-teams-notifications Docker container to AWS Lambda. The workflow automates the process of building a Docker image, pushing it to Amazon Elastic Container Registry (ECR), and updating the AWS Lambda function to use the latest image. This setup utilizes OpenID Connect (OIDC) for secure AWS authentication without storing AWS credentials as secrets in GitHub.

## Workflow Overview

The GitHub Action is triggered on push events to the `main` branch that affect any files from the following paths:
- [utilities/ms-teams-notifications/src/**](/utilities/ms-teams-notifications/src/)
- [utilities/ms-teams-notifications/Dockerfile](/utilities/ms-teams-notifications/Dockerfile)
- [utilities/common/src/aws_utilities.py](/utilities/common/src/aws_utilities.py)
- [.github/workflows/ms-teams-notifications.yml](/.github/workflows/ms-teams-notifications.yml)

The action performs the following steps:

1. **Checkout Repository**: Clones the repository to the GitHub Actions runner.
2. **Configure AWS Credentials**: Uses OIDC to authenticate with AWS and assume an IAM role specified by a secret in the GitHub repository.
3. **Login to Amazon ECR**: Authenticates the Docker client to your Amazon ECR registry.
4. **Build, Tag, and Push Image to Amazon ECR**: Builds a Docker image from [utilities/ms-teams-notifications/Dockerfile](/utilities/ms-teams-notifications/Dockerfile), tags it, and pushes it to the specified ECR repository.
5. **Update Lambda Function to Use the Latest Image**: Updates the AWS Lambda function to use the newly pushed Docker image.

## Dockerfile Overview

This Dockerfile uses an official AWS Lambda runtime image for Python 3.12 as its base. It installs necessary Python packages (requests, boto3, etc) and copies the Lambda function code ([app.py](/utilities/ms-teams-notifications/src/app.py)) and shared custom library ([aws_utilities.py](/utilities/common/src/aws_utilities.py)) into the image. The CMD instruction specifies the function handler.

## Prerequisites
Before deploying this workflow, ensure that:

 - The AWS ECR repository exists and is accessible by the IAM role.

 - The IAM role specified in AWS_ROLE_ARN has permissions for ECR operations and Lambda function updates.

 - The AWS Lambda function temp-access-update-notifications exists and is configured to use a container image from ECR.