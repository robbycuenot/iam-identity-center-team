resource "aws_ecr_repository" "ms-teams-notifications" {
  name                 = "ms-teams-notifications"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  # Enables the encryption of images at rest
  encryption_configuration {
    encryption_type = "AES256"
  }
}

resource "aws_ecr_repository" "temp-access-update-notifications" {
  name                 = "temp-access-update-notifications"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  # Enables the encryption of images at rest
  encryption_configuration {
    encryption_type = "AES256"
  }
}
