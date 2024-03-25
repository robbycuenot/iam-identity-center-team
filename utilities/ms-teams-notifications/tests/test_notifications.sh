#!/bin/bash

# Define the path to the JSON files for notifications
SNS_FILE="./utilities/ms-teams-notifications/tests/sns_event.json"

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

# Function to process files based on input parameters
function process_files() {
    local current_user_upn="$1"
    local current_user_email="$2"
    
    # Shift the first two arguments so that "$@" now represents only the file paths
    shift 2
    
    # Now assign the remaining arguments to the files array correctly
    local files=("$@")

    for request_file in "${files[@]}"; do
        # Initialize the path for a corresponding payload file
        local payload_file_path="./utilities/ms-teams-notifications/tests/sample-json/payloads/$(basename "$request_file")"
        
        # Check for the existence of a payload file and process it
        local processed_payload=""
        if [ -f "$payload_file_path" ]; then
            # Replace placeholders in the payload file
            processed_payload=$(sed -e "s/CURRENTUSERUPN/$current_user_upn/g" -e "s/CURRENTUSEREMAIL/$current_user_email/g" "$payload_file_path")
            # Double-escape and prepare the payload for insertion
            processed_payload=$(echo "$processed_payload" | jq -c . | jq -aRs . | jq -aRs . | sed 's/^"//;s/\\n\\"\\n"$/"/')
        fi

        # Modify the main message file to replace placeholders
        local message_body=$(sed -e "s/CURRENTUSERUPN/$current_user_upn/g" -e "s/CURRENTUSEREMAIL/$current_user_email/g" "$request_file")
        # Escape the message for JSON
        message_body=$(echo "$message_body" | jq -c .)
        
        # If there's a processed payload, insert it into the message body
        if [[ ! -z "$processed_payload" ]]; then
            if [[ ! -z "$processed_payload" ]]; then
                # Using sed to replace "PAYLOAD_PLACEHOLDER" in the already-escaped JSON string
                # Note: This requires careful handling of escape characters in the sed pattern
                message_body=$(echo "$message_body" | sed "s|\"PAYLOAD_PLACEHOLDER\"|$processed_payload|")
            fi
        fi

        # Prepare the final SNS event JSON for the Lambda function
        local sns_event=$(jq --arg msg "$message_body" '.Records[0].Sns.Message = $msg' "$SNS_FILE")

        # Print the name of the request file being processed
        echo "Sending $(basename "$request_file" .json) request..."

        # Invoke the Lambda function with the modified payload
        curl -sS -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d "$sns_event" | jq

        echo ""

        # Sleep to avoid rate limits
        sleep 1
    done
}


# Main script logic

# Fetch user and system information
echo "Fetching current user information..."
CURRENT_USER_UPN=$(get_current_user_upn)
IDENTITY_STORE_ID=$(get_identity_store_id)
CURRENT_USER_ID=$(get_current_user_id "$IDENTITY_STORE_ID" "$CURRENT_USER_UPN")
CURRENT_USER_EMAIL=$(get_current_user_email "$IDENTITY_STORE_ID" "$CURRENT_USER_ID")

# Determine which files to process based on script parameters
if [ "$#" -eq 0 ]; then
    # No parameters, process all sample JSON files in the immediate directory only
    FILES=() # Initialize array
    for file in ./utilities/ms-teams-notifications/tests/sample-json/*.json; do
        if [ -f "$file" ]; then # Ensure it's a file, not a directory
            FILES+=("$file")
        fi
    done
else
    # Parameters specified, process only those files
    FILES=()
    for PARAM in "$@"; do
        FILES+=("./utilities/ms-teams-notifications/tests/sample-json/$PARAM.json")
    done
fi


# Process the files
process_files "$CURRENT_USER_UPN" "$CURRENT_USER_EMAIL" "${FILES[@]}"
