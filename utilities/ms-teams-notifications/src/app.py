import json
import os
import logging
from aws_utilities import (
    get_amplify_app_id_from_name,
    get_identitystoreid,
    get_user_from_email
)
from teams_communication import (
    construct_teams_message,
    send_teams_message
)

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

region = os.getenv('AWS_REGION', 'us-east-1')
app_name = 'TEAM-IDC-APP'

def lambda_handler(event, context):
    # Log the received SNS event
    logger.info("Received event: %s", json.dumps(event))
    sns_message = event['Records'][0]['Sns']['Message']

    # Log the received SNS message
    logger.info("Received SNS message: %s", sns_message)
    
    # Assuming the SNS message is a stringified JSON
    message = json.loads(sns_message)

    # Extract the payload from the message if it exists
    payload = extract_payload(message)

    # Common details extracted from the message
    email = message.get('email', 'N/A')
    approver_emails = message.get('approvers', 'N/A')
    
    # Get the Identity Store ID
    identitystoreid = get_identitystoreid()

    # Get the user details for the requester
    user = get_user_from_email(identitystoreid, email)

    # Get the user details for each approver
    approver_users = []
    for approver_email in approver_emails:
        approver_user = get_user_from_email(identitystoreid, approver_email)
        approver_users.append(approver_user)

    # Get the user details for the approved by user, if it exists
    approved_by_users = []
    if message.get('approver', None):
        try:
            approved_by_email = message.get('approver', None)
            approved_by_user = get_user_from_email(identitystoreid, approved_by_email)
            approved_by_users.append(approved_by_user)
        except Exception as e:
            logger.info("Error retrieving approver user.")
            pass

    # Get the user details for the rejected by user, if it exists
    rejected_by_users = []
    if message.get('status').lower() == 'rejected':
        try:
            rejected_by_email = message.get('approver', None)
            rejected_by_user = get_user_from_email(identitystoreid, rejected_by_email)
            rejected_by_users.append(rejected_by_user)
        except Exception as e:
            logger.info("Error retrieving rejector user.")
            pass

    # Get the user details for the revoked by user, if it exists
    revoked_by_users = []
    if message.get('status').lower() == 'ended':
        if message.get('data', {}).get('Item', {}).get('status', {}).get('S', 'ended') == 'revoked':
            try:
                revoked_by_email = message.get('data').get('Item').get('revoker').get('S')
                revoked_by_user = get_user_from_email(identitystoreid, revoked_by_email)
                revoked_by_users.append(revoked_by_user)
            except Exception as e:
                logger.info("Error retrieving revoker user.")
                pass

    # Get the link to the approvals page in the TEAM-IDC-APP
    amplify_app_id = get_amplify_app_id_from_name(app_name)
    message['approval_url'] = f"https://main.{amplify_app_id}.amplifyapp.com/approvals/approve"

    # Construct the message for Microsoft Teams based on status
    teams_message = construct_teams_message(user, approver_users, approved_by_users, rejected_by_users, revoked_by_users, message, payload)
    
    # Send the message to Microsoft Teams
    send_teams_message_result = send_teams_message(teams_message)
    if send_teams_message_result.get('statusCode') != 200:
        logger.error("Failed to send message to Microsoft Teams.")
    
    # Return a success response or handle errors as needed
    return {
        'statusCode': 200,
        'body': json.dumps('Function execution completed.')
    }

def extract_payload(message_details):
    """
    Attempts to extract the nested payload object from 'Payload.Payload.body' or 'lastTaskResult.Payload.body' if it exists.
    """
    try:
        # Attempt to decode the nested payload from 'Payload.Payload.body'
        payload_body = message_details.get('Payload', {}).get('Payload', {}).get('body', None)
        if not payload_body:
            # If 'Payload.Payload.body' is not found, try 'lastTaskResult.Payload.body'
            payload_body = message_details.get('lastTaskResult').get('Payload').get('body')
        
        # If a payload was found, log it and return it
        if payload_body:
            logger.info(f"Payload: {payload_body}")
            payload = json.loads(payload_body)
            return payload.get('data').get('updateRequests')

    except Exception as e:
        logger.info("No payload found in the message.")
        return None

    return None

if __name__ == "__main__":
    # This allows the file to be executed as a script for testing
    lambda_handler({}, {})
