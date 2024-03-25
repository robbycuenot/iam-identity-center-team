# Infrastructure Configuration for temp-access-update-notifications

This Terraform configuration deploys an AWS Lambda function that sends notifications to a Microsoft Teams channel via a Webhook connector. It includes resources for creating an Amazon ECR repository for the Lambda function's Docker image, IAM roles and policies for the Lambda execution and GitHub Actions integration, and the CloudWatch event rule that triggers the Lambda.

## Resources

### AWS ECR Repository (`aws_ecr_repository`)

- **Name**: `temp-access-update-notifications` - The name of the ECR repository.
- **Image Tag Mutability**: `MUTABLE` - Allows image tags to be overwritten.
- **Image Scanning Configuration**: Enabled to scan images on push.
- **Encryption Configuration**: Uses AES256 encryption for images at rest.

### AWS IAM OpenID Connect Provider (`aws_iam_openid_connect_provider`)

- Configures an OIDC provider for GitHub to allow GitHub Actions to assume an IAM role.

### IAM Policies (`aws_iam_policy`)

- **GitHub ECR Policy (`aws_iam_policy.github_ecr_policy`)**: Allows GitHub Actions to push images to the ECR repository and update the Lambda function code.
- **Lambda Execution Role Policy (`aws_iam_policy.lambda_logging`, `aws_iam_policy.lambda_sso_readonly`, `aws_iam_policy.lambda_amplify_readonly`)**: Grants the Lambda function permissions for logging, accessing AWS SSO, and AWS Amplify.

### IAM Roles

- **GitHub Actions Role (`aws_iam_role.github_actions`)**: Allows GitHub Actions to assume this role through OIDC.
- **Lambda Execution Role (`aws_iam_role.temp-access-update-notifications-lambda_execution_role`)**: The execution role for the Lambda function, granting it permissions defined in attached policies.

### Lambda Function (`aws_lambda_function.temp-access-update-notifications`)

- Deploys the Lambda function using a Docker image from the ECR repository.
- Configured with an environment variable for the Teams Webhook URL.

### CloudWatch Event Rule (`aws_cloudwatch_event_rule.temp-access-update-notifications-daily_trigger`)

- The trigger for the Lambda to fire on a schedule

### CloudWatch Event Target (`aws_cloudwatch_event_target.temp-access-update-notifications-invoke_lambda_daily`)

- The target for the rule to invoke

## Variables

- **TEAMS_WEBHOOK_URL**: The URL of the Microsoft Teams Webhook connector. Marked as sensitive.

## Terraform Cloud Configuration

Specifies the required Terraform version and configures the backend for Terraform Cloud, targeting a specific workspace and organization.

## Provider

Defines the AWS provider and specifies the AWS region.

## Usage

To deploy this configuration:

1. Navigate to the terraform workspace
1. Ensure that OIDC is configured properly in the target account and workspace variables
1. Set the `TEAMS_WEBHOOK_URL` to the url of the desired channel webhook
1. Plan and apply 🚀

## Security Considerations

- Ensure the `TEAMS_WEBHOOK_URL` is kept secure and is only accessible to authorized personnel.