resource "aws_cloudwatch_event_target" "temp-access-update-notifications-invoke_lambda" {
  rule      = aws_cloudwatch_event_rule.temp-access-update-notifications-trigger.name
  target_id = "InvokeLambda"
  arn       = aws_lambda_function.temp-access-update-notifications.arn
}
