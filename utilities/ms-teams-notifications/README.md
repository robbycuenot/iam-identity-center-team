# AWS Lambda Function for ms-teams-notifications

This AWS Lambda function is designed to send notifications to a Microsoft Teams channel through a Webhook connector. It specifically supports notifications for AWS Temporary Elevated Access Notifications (AWS TEAM), such as access requests, approvals, rejections, cancellations, and status updates.

## Additional Documentation

Additional documentation regarding the MS Teams integration and development can be found under [docs/](docs/)

## Functionality

The function performs the following actions:

1. Receives an SNS message triggered by an event related to AWS Temporary Elevated Access.
2. Extracts details from the message, such as requester's email, approver emails, SSO instance ARN, and other relevant information.
3. Retrieves additional user information from AWS SSO Identity Store based on the extracted details.
4. Constructs a notification message tailored to the specific event status (e.g., pending, approved, rejected).
5. Sends the constructed message to a specified Microsoft Teams channel via a Webhook URL.

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
- `datetime`: For parsing and formatting dates and times.
- `logging`: Standard logging library.
- `json`: Standard JSON library for parsing and constructing JSON objects.
- `os`: Standard library for accessing environment variables.
- `requests`: A simple HTTP library for Python. Used to send the notification message to Microsoft Teams.
- `re`: A regex library for matching patterns.
- [common/aws_utilities.py](/utilities/common/src/aws_utilities.py): A library shared between lambdas with common AWS tasks.

## Input Format

The function expects an SNS message in a JSON format, containing details about the AWS TEAM event, such as:

```json
{
  "email": "requestor@example.com",
  "approvers": ["approver1@example.com", "approver2@example.com"],
  "instanceARN": "arn:aws:sso:::instance/ssoins-1234567890123456",
  "time": "2",
  "accountName": "Development Account",
  "accountId": "123456789012",
  "role": "AdministratorAccess",
  "justification": "For deployment purposes",
  "status": "pending",
  "startTime": "2023-01-01T00:00:00Z"
}
```

## Output

The function logs the status of the message delivery to Microsoft Teams and returns a status code indicating success (200) or failure along with an error message.

## Error Handling

If the TEAMS_WEBHOOK_URL environment variable is not set, the function logs an error and returns a 400 status code with an appropriate error message. If the message fails to send to Microsoft Teams, it logs the failure and returns the response status code from the Teams Webhook call.