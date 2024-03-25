resource "aws_iam_role" "github_actions" {
  name               = "GitHubActionsRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Federated = aws_iam_openid_connect_provider.github.arn
        },
        Action = "sts:AssumeRoleWithWebIdentity",
        Condition = {
          StringEquals = {
            "${aws_iam_openid_connect_provider.github.url}:aud" = "sts.amazonaws.com",
          },
          "StringLike": {
            "${aws_iam_openid_connect_provider.github.url}:sub": "repo:${var.AWS_TEAM_GITHUB_REPO}:ref:refs/heads/main",
          }
        }
      },
    ],
  })
}

resource "aws_iam_role" "ms-teams-notifications-lambda_execution_role" {
  name = "ms-teams-notifications-lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
        Effect = "Allow",
        Sid = "",
        Condition = {
          StringEquals = {
            "aws:SourceArn": "arn:aws:lambda:${var.AWS_REGION}:${data.aws_caller_identity.current.account_id}:function:ms-teams-notifications"
          }
        }
      },
    ]
  })
}

resource "aws_iam_role" "temp-access-update-notifications-lambda_execution_role" {
  name = "temp-access-update-notifications-lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
        Effect = "Allow",
        Sid = "",
        Condition = {
          StringEquals = {
            "aws:SourceArn": "arn:aws:lambda:${var.AWS_REGION}:${data.aws_caller_identity.current.account_id}:function:temp-access-update-notifications"
          }
        }
      },
    ]
  })
}
