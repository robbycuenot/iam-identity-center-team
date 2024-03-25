data "aws_sns_topic" "team_notifications" {
  name = "TeamNotifications-main"
}

data "aws_codecommit_repository" "team-idc-app" {
  repository_name = "team-idc-app"
}

data "aws_caller_identity" "current" {}

data "tls_certificate" "github_actions" {
  url = "https://token.actions.githubusercontent.com"
}
