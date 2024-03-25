resource "aws_iam_role_policy_attachment" "github_ecr_policy_attach" {
  role       = aws_iam_role.github_actions.name
  policy_arn = aws_iam_policy.github_ecr_policy.arn
}

resource "aws_iam_role_policy_attachment" "ms-teams-notifications-lambda_logs" {
  role       = aws_iam_role.ms-teams-notifications-lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

resource "aws_iam_role_policy_attachment" "ms-teams-notifications-lambda_sso_readonly" {
  role       = aws_iam_role.ms-teams-notifications-lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_sso_readonly.arn
}

resource "aws_iam_role_policy_attachment" "ms-teams-notifications-lambda_amplify_readonly" {
  role       = aws_iam_role.ms-teams-notifications-lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_amplify_readonly.arn
}

resource "aws_iam_role_policy_attachment" "temp-access-update-notifications-lambda_logs" {
  role       = aws_iam_role.temp-access-update-notifications-lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

resource "aws_iam_role_policy_attachment" "temp-access-update-notifications-lambda_sso_readonly" {
  role       = aws_iam_role.temp-access-update-notifications-lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_sso_readonly.arn
}

resource "aws_iam_role_policy_attachment" "temp-access-update-notifications-lambda_amplify_readonly" {
  role       = aws_iam_role.temp-access-update-notifications-lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_amplify_readonly.arn
}

resource "aws_iam_role_policy_attachment" "temp-access-update-notifications-lambda_codecommit_access" {
role = aws_iam_role.temp-access-update-notifications-lambda_execution_role.name
policy_arn = aws_iam_policy.lambda_codecommit_access.arn
}