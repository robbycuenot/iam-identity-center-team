# Developing and Testing ms-teams-notifications

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

1. **Configure Test Data**: Sample data for each request type is provided under [tests/sample-json/](/utilities/ms-teams-notifications/tests/sample-json/). This data contains placeholder values for email addresses. At runtime, the AWS credentials provided in the previous step will be used to query your email address from the AWS Identity Store. The placeholder value will be substituted in memory before the request is sent, to ensure that tests only notify the person running them.

1. **Running the App**: A simple startup script is provided at [tests/start_notifications.sh](/utilities/ms-teams-notifications/tests/start_notifications.sh). An alias is injected at buildtime in the codespace to make this easier to run. Open a terminal and run `start_notifications` and the container will build and start. If running outside of codespaces, this can be invoked with the following command:
```
./utilities/ms-teams-notifications/tests/start_notifications.sh
```

1. **Testing the App**: Similar to the startup script, a testing script is provided at [tests/test_notifications.sh](/utilities/ms-teams-notifications/tests/test_notifications.sh), and is aliased to `test_notifications`. Running this script requires creating a second terminal; it is recommended to split the container terminal so that the output of both the lambda and the script are visible. This second terminal will also need to have AWS credentials injected. Running this command without parameters will test each of the json files under [tests/sample-json/](/utilities/ms-teams-notifications/tests/sample-json/). Providing one or more of the file names (without .json) as arguments will test those files. 
     - Examples:
        - `test_notifications`
        - `test_notifications approved granted`
        - If running outside of codespaces:
         - `./utilities/ms-teams-notifications/tests/start_notifications.sh`
         - `./utilities/ms-teams-notifications/tests/start_notifications.sh approved granted`

1. **Iterating**: Any changes to the [Dockerfile](/utilities/ms-teams-notifications/Dockerfile) or underlying code will not be reflected until the container has restarted. Simply `Ctrl+C` in the container terminal and rerun `start_notifications` to test modifications.