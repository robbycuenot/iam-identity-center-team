variable "AWS_REGION" {
  type      = string
  sensitive = false
  default = "us-east-1"
}

variable "AWS_TEAM_GITHUB_REPO" {
  type      = string
  sensitive = false
}

variable "TEAMS_WEBHOOK_URL" {
  type      = string
  sensitive = true
}

variable "UPDATE_NOTIFICATION_GROUP" {
  type      = string
  sensitive = false
  default   = null
}

variable "UPDATE_NOTIFICATION_USER_EMAIL" {
  type      = string
  sensitive = false
  default   = null
}
