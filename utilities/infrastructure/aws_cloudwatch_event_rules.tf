resource "aws_cloudwatch_event_rule" "temp-access-update-notifications-trigger" {
  name                = "temp-access-update-notifications-trigger"
  description         = "Triggers the temp-access-update-notifications Lambda function"
  schedule_expression = "cron(0 18 ? * WED *)"
}