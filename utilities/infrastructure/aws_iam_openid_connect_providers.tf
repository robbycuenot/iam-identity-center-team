resource "aws_iam_openid_connect_provider" "github" {
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = data.tls_certificate.github_actions.certificates.*.sha1_fingerprint
  url             = "https://token.actions.githubusercontent.com"
}
