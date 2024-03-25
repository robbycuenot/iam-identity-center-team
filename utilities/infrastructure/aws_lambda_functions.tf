resource "aws_lambda_function" "ms-teams-notifications" {
  function_name = "ms-teams-notifications"

  package_type = "Image"
  image_uri    = "${aws_ecr_repository.ms-teams-notifications.repository_url}:latest"

  role    = aws_iam_role.ms-teams-notifications-lambda_execution_role.arn
  timeout = 60 # Adjust based on your function's expected execution time

  environment {
    variables = {
      TEAMS_WEBHOOK_URL = var.TEAMS_WEBHOOK_URL
    }
  }
}

resource "aws_lambda_function" "temp-access-update-notifications" {
  function_name = "temp-access-update-notifications"

  package_type = "Image"
  image_uri    = "${aws_ecr_repository.temp-access-update-notifications.repository_url}:latest"

  role    = aws_iam_role.temp-access-update-notifications-lambda_execution_role.arn
  timeout = 60 # Adjust based on your function's expected execution time

  environment {
    variables = {
      TEAMS_WEBHOOK_URL = var.TEAMS_WEBHOOK_URL
      UPDATE_NOTIFICATION_GROUP = var.UPDATE_NOTIFICATION_GROUP
      UPDATE_NOTIFICATION_USER_EMAIL = var.UPDATE_NOTIFICATION_USER_EMAIL
    }
  }
}
