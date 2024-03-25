resource "aws_lambda_permission" "allow_sns" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ms-teams-notifications.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = data.aws_sns_topic.team_notifications.arn
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.temp-access-update-notifications.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.temp-access-update-notifications-trigger.arn
}
