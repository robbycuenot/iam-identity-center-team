# Function to get the current user's UPN (User Principal Name) from AWS
function get_current_user_upn() {
    aws sts get-caller-identity | jq -r .UserId | cut -d':' -f2
}

# Function to get the identity store ID to query user information
function get_identity_store_id() {
    aws sso-admin list-instances | jq -r .Instances[0].IdentityStoreId
}

# Function to get the current user's ID using their UPN
function get_current_user_id() {
    local identity_store_id="$1"
    local upn="$2"
    aws identitystore get-user-id --identity-store-id "$identity_store_id" --alternate-identifier "{\"UniqueAttribute\":{\"AttributePath\": \"userName\", \"AttributeValue\": \"$upn\"}}" | jq -r .UserId
}

# Function to get the current user's email
function get_current_user_email() {
    local identity_store_id="$1"
    local user_id="$2"
    aws identitystore describe-user --identity-store-id "$identity_store_id" --user-id "$user_id" | jq -r '.Emails[] | select(.Primary == true) | .Value'
}

echo "Fetching current user information..."
CURRENT_USER_UPN=$(get_current_user_upn)
IDENTITY_STORE_ID=$(get_identity_store_id)
CURRENT_USER_ID=$(get_current_user_id "$IDENTITY_STORE_ID" "$CURRENT_USER_UPN")
CURRENT_USER_EMAIL=$(get_current_user_email "$IDENTITY_STORE_ID" "$CURRENT_USER_ID")

docker build -t temp-access-update-notifications -f utilities/temp-access-update-notifications/Dockerfile utilities

docker run \
  --rm \
  -d \
  --name temp-access-update-notifications \
  -e TEAMS_WEBHOOK_URL=$TEST_CHANNEL_WEBHOOK \
  -e UPDATE_NOTIFICATION_USER_EMAIL=$CURRENT_USER_EMAIL \
  -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  -e AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN \
  -e AWS_REGION=$AWS_REGION \
  --platform linux/amd64 \
  -p 9001:8080 \
  temp-access-update-notifications

# Wait for the container to start
sleep 5

curl -sS -XPOST "http://localhost:9001/2015-03-31/functions/function/invocations" -d "{}" | jq

docker stop temp-access-update-notifications