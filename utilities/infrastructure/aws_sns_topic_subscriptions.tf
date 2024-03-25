resource "aws_sns_topic_subscription" "lambda_subscription" {
  topic_arn = data.aws_sns_topic.team_notifications.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.ms-teams-notifications.arn
}
