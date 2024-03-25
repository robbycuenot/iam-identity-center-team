docker build -t ms-teams-notifications -f utilities/ms-teams-notifications/Dockerfile utilities

docker run \
  --rm \
  --name ms-teams-notifications \
  -e TEAMS_WEBHOOK_URL=$TEST_CHANNEL_WEBHOOK \
  -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  -e AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN \
  -e AWS_REGION=$AWS_REGION \
  --platform linux/amd64 \
  -p 9000:8080 \
  ms-teams-notifications