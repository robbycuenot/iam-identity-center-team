# AWS Lambda Functions for Microsoft Teams

Two custom AWS Lambda functions have been created to send notifications to a Microsoft Teams channel through a Webhook connector:
 - [ms-teams-notifications](/utilities/ms-teams-notifications/README.md)
 - [temp-access-update-notifications](/utilities/temp-access-update-notifications/README.md)

The former sends AWS Temporary Elevated Access Notifications (AWS TEAM), such as access requests, approvals, rejections, cancellations, and status updates.

The latter sends a once-weekly reminder that a new version of AWS TEAM is available on GitHub, and mentions the designated parties.
