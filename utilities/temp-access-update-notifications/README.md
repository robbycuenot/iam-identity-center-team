# AWS Lambda Function for temp-access-update-notifications

This AWS Lambda function is designed to send notifications to a Microsoft Teams channel through a Webhook connector. It specifically sends a notification when a version newer than the currently deployed version is available on GitHub.

## Additional Documentation

Additional documentation regarding the development, testing, and infrastructure can be found under [docs/](docs/)

## Functionality

The function performs the following actions:

1. Waits for a trigger from AWS EventBridge to execute
1. Queries GitHub for the latest version of AWS TEAM
1. Queries the codecommit repo for the currently deployed version of AWS TEAM
1. Compares the versions
1. If a newer version is available:
    1. Gets the list of users to notify
    1. Builds a message with the version differences and release notes
    1. Sends the message
1. If the versions match:
    1. Does not send a message, but logs the match to cloudwatch


## Environment Variables

- `AWS_REGION`: Specifies the AWS Region where the function operates. Default is `us-east-1`.
    - The lambda sets this to the current region by default. Only specify this if running locally or in a region different than the IAM Identity Center instance.
- `TEAMS_WEBHOOK_URL`: The URL of the Microsoft Teams Webhook connector where notifications will be sent.

If developing in GitHub Codespaces, it is encouraged to add these values as codespace secrets for testing.

If developing locally, these environment variables will need to be set with `export` commands.

When running on AWS Lambda, these environment variables need to be set in the lambda configuration.

## Required Permissions

The Lambda function requires permissions to access various AWS services, including:

- SSO Admin (`sso-admin`) to retrieve the identity store ID.
- Identity Store (`identitystore`) to get user details.
- Amplify (`amplify`) to retrieve the Amplify app ID for constructing approval URLs.

## Dependencies

- `boto3`: AWS SDK for Python. Used to interact with AWS services.
- `logging`: Standard logging library.
- `json`: Standard JSON library for parsing and constructing JSON objects.
- `os`: Standard library for accessing environment variables.
- `requests`: A simple HTTP library for Python. Used to send the notification message to Microsoft Teams.
- [common/aws_utilities.py](/utilities/common/src/aws_utilities.py): A library shared between lambdas with common AWS tasks.

## Input Format

The function does not expect any particular input, only a `POST` request. A simple message with a blank payload can be sent:

```json
{}
```

## Output

The function logs the status of the message delivery to Microsoft Teams and returns a status code indicating success (200) or failure along with an error message.

## Error Handling

If the TEAMS_WEBHOOK_URL environment variable is not set, the function logs an error and returns a 400 status code with an appropriate error message. If the message fails to send to Microsoft Teams, it logs the failure and returns the response status code from the Teams Webhook call.