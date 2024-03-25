# Developing and Testing temp-access-update-notifications

This guide covers the setup and testing of the AWS Lambda application for sending notifications to Microsoft Teams, and (optionally, but recommended) using GitHub Codespaces. Codespaces provides a fully configured development environment in the cloud, allowing you to develop and test the application without needing to set up your local environment.

## Prerequisites

Before you start, ensure you have the following:
- (optional) A GitHub account with access to Codespaces.
- The necessary permissions to access the AWS resources and services used by this application.
- `AWS_REGION` and `TEST_CHANNEL_WEBHOOK` stored as Codespace secrets for testing, or be ready to export them as environment variables.
- AWS SSO ReadOnly credentials for the TEAM account.

## Configuring Codespaces

If using Codespaces, when you launch a new codespace for the project, it is built using the specified Dockerfile and configurations. The Codespace includes tools and extensions necessary for development, such as the AWS CLI, Terraform, and GitHub Copilot.

### Codespace Dockerfile Configuration

The Codespace environment is based on the Microsoft universal image and includes the following configurations:
- **AWS CLI**: Installed and configured for command-line access to AWS services.
- **Terraform CLI**: Installed for infrastructure as code management.
- **Aliases**: Custom aliases for Terraform and test scripts are added for convenience.

## Developing and Testing

### Setting Environment Variables

1. **AWS Region and Webhook URL**: Ensure you have `AWS_REGION` and `TEST_CHANNEL_WEBHOOK` set as Codespace secrets or export them in the terminal.
   ```bash
   export AWS_REGION='your-aws-region'
   export TEST_CHANNEL_WEBHOOK='your-test-channel-webhook-url'
   ```

1. **AWS Temporary R/O Credentials**: Navigate to the AWS SSO login page, select the TEAM account, and click "Command line or programmatic access" next to a read-only role. Copy and paste the export commands to your terminal.
    ```bash
    export AWS_ACCESS_KEY_ID="ASABCDWZV4MC7..."
    export AWS_SECRET_ACCESS_KEY="NaWTctnevody5oVFzwMs/..."
    export AWS_SESSION_TOKEN="IQoJb3JpZ2luX......"
    ```

1. **Testing the App**: A simple startup script is provided at [tests/test_update_notifications.sh](/utilities/temp-access-update-notifications/tests/test_update_notifications.sh). An alias is injected at buildtime in the codespace to make this easier to run. Open a terminal and run `test_update_notifications` and the script will start. If running outside of codespaces, this can be invoked with the following command:
```
./utilities/temp-access-update-notifications/tests/test_update_notifications.sh
```

The script performs the following actions:
1. Uses the shell's environment variables to query AWS for the current user's email
1. Builds the docker container
1. Starts the docker container in the background, injecting:
   - The current user's email
   - The TEST_CHANNEL_WEBHOOK environment variable
   - The AWS_REGION environment variable
   - The AWS Read-Only credentials from the shell
1. Sends a blank payload to invoke the lambda_event_handler within the container
1. Prints the response
1. Stops and removes the container

This allows for rapid iteration and testing. As changes are made to the code, they can be tested by running `test_update_notifications` repeatedly.

An successful run will resemble this:
```bash
@yourusername ➜ /workspaces/iam-identity-center-team (main) $ test_update_notifications
Fetching current user information...
[+] Building 0.8s (9/9) FINISHED                                                        docker:default
 => [internal] load build definition from Dockerfile                                              0.1s
 => => transferring dockerfile: 433B                                                              0.0s
 => [internal] load .dockerignore                                                                 0.1s
 => => transferring context: 2B                                                                   0.0s
 => [internal] load metadata for public.ecr.aws/lambda/python:3.12                                0.2s
 => [1/4] FROM public.ecr.aws/lambda/python:3.12@sha256:9ace63fcbbf8d96d889a8f4cd70f716ccf93fa91  0.0s
 => [internal] load build context                                                                 0.1s
 => => transferring context: 662B                                                                 0.0s
 => CACHED [2/4] RUN pip install requests boto3>=1.34.42                                          0.0s
 => CACHED [3/4] COPY temp-access-update-notifications/src/*.py ./                                0.0s
 => CACHED [4/4] COPY common/src/aws_utilities.py ./                                              0.0s
 => exporting to image                                                                            0.0s
 => => exporting layers                                                                           0.0s
 => => writing image sha256:0d79e9383e4ba72962316236422a17da3c9f307aa121b472b2231f6843dce470      0.0s
 => => naming to docker.io/library/temp-access-update-notifications                               0.0s
e30202677abea57fbd167583a10b2e1ff15e1c0dad069991002ed9b714be366f
{
  "statusCode": 200,
  "body": "{\"message\": \"New version detected on GitHub. Notification sent to Microsoft Teams.\", \"github_version\": \"v1.1.1\", \"codecommit_version\": \"v1.1.0\"}"
}
temp-access-update-notifications
```