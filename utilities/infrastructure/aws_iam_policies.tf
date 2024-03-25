resource "aws_iam_policy" "github_ecr_policy" {
  name        = "GitHubActionsECRPolicy"
  description = "Policy for GitHub Actions to push to ECR"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        "Effect": "Allow",
        "Action": [
          "ecr:GetAuthorizationToken"
        ],
        "Resource": "*"
      },
      {
        "Effect": "Allow",
        "Action": [
          "ecr:BatchCheckLayerAvailability",
          "ecr:CompleteLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:InitiateLayerUpload",
          "ecr:PutImage"
        ],
        "Resource": [
          "${aws_ecr_repository.ms-teams-notifications.arn}",
          "${aws_ecr_repository.temp-access-update-notifications.arn}"
        ]
      },
      {
        "Effect": "Allow",
        "Action": "lambda:UpdateFunctionCode",
        "Resource": [
            "${aws_lambda_function.ms-teams-notifications.arn}",
            "${aws_lambda_function.temp-access-update-notifications.arn}"
        ]
      }
    ],
  })
}

resource "aws_iam_policy" "lambda_logging" {
  name        = "lambda_logging_policy"
  description = "IAM policy for logging from a lambda"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "arn:aws:logs:*:*:*",
        Effect   = "Allow",
      },
    ]
  })
}

resource "aws_iam_policy" "lambda_sso_readonly" {
  name        = "lambda_sso_readonly"
  description = "IAM policy for retrieving user information from AWS SSO"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "identitystore:GetUserId",
          "identitystore:GetGroupId",
          "identitystore:GetGroupMembershipId",
          "identitystore:DescribeUser",
          "identitystore:DescribeGroup",
          "identitystore:DescribeGroupMembership",
          "identitystore:ListUsers",
          "identitystore:ListGroups",
          "identitystore:ListGroupMemberships",
          "sso:ListInstances"
        ],
        Resource = "*",
        Effect   = "Allow",
      },
    ]
  })
}

resource "aws_iam_policy" "lambda_amplify_readonly" {
  name        = "lambda_amplify_readonly"
  description = "IAM policy for retrieving information from AWS Amplify"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "amplify:ListApps",
          "amplify:GetApp",
          "amplify:GetBranch",
        ],
        Resource = "*",
        Effect   = "Allow",
      },
    ]
  })
}

resource "aws_iam_policy" "lambda_codecommit_access" {
  name        = "lambda_codecommit_access_policy"
  description = "IAM policy for accessing CodeCommit repositories from a lambda"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "codecommit:GetFile",
          "codecommit:GetRepository"
        ],
        Resource = "${data.aws_codecommit_repository.team-idc-app.arn}",
        Effect   = "Allow",
      },
    ]
  })
}
