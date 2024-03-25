import json
import logging
import os
import requests
from datetime import datetime, timezone

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def construct_teams_message(user, approver_users, approved_by, rejected_by, revoked_by, message_details, payload=None):
    """
    Constructs the message payload for Microsoft Teams based on the status and other details.
    """
    status = message_details.get('status', 'N/A').lower()
    activityTitle = get_activity_title(status)

    # On "pending" status, check the payload for a status and use it if available
    if status == "pending" and payload:
        status = payload.get('status', status)
        activityTitle = get_activity_title(status)
    # On "approved" status, check the payload for a status and use it if available
    elif status == "approved" and payload:
        try:
            status = payload.get('status', status)
            if status == "scheduled":
                startTime = payload.get('startTime', 'N/A')
                startTime = datetime.strptime(startTime, "%Y-%m-%dT%H:%M:%S%z")
                startTime = startTime.astimezone(timezone.utc)
                if startTime > datetime.now(timezone.utc):
                    activityTitle = get_activity_title(status)
        except Exception as e:
            logger.info(f"Error parsing scheduled start time: {e}")
            pass
    # On "ended" status, check the data object for a status and use it if available
    elif status == "ended":
        try:
            sub_status = message_details.get('data').get('Item').get('status').get('S')
            logger.info(f"Substatus found for ended status: {sub_status}")
            if sub_status == "revoked":
                activityTitle = get_activity_title(sub_status)
        except Exception as e:
            logger.info(f"No substatus found for ended status. Using default status.")
            pass

    # Only mention approvers if the status is "pending"
    approver_mentions = get_approver_mentions_from_status(status, approver_users)
    approved_by_mentions = get_approver_mentions_from_status(status, approved_by)
    rejected_by_mentions = get_approver_mentions_from_status(status, rejected_by)
    revoked_by_mentions = get_approver_mentions_from_status(status, revoked_by)

    teams_message = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "body": [
                        {
                            "type": "TextBlock",
                            "size": "Large",
                            "weight": "Bolder",
                            "text": activityTitle
                        },
                        {
                            "type": "ColumnSet",
                            "columns": [
                                create_column_one(message_details, user, approver_mentions, approved_by_mentions, rejected_by_mentions, revoked_by_mentions),
                                create_column_two(message_details)
                            ]
                        }
                    ],
                    "selectAction": {
                        "type": "Action.OpenUrl",
                        "title": "View in AWS",
                        "url": message_details.get('approval_url', 'N/A')
                    },
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.0",
                    "msteams": {
                        "width": "Full",
                        "entities": create_mentions(user, approver_users, status)
                    }
                }
            }
        ]
    }

    logger.info(f"Constructed message for Microsoft Teams: {teams_message}")

    return teams_message


def get_activity_title(status):
    """
    Returns the title text based on the request status.
    """
    titles = {
        "pending": "🚀 New Access Request",
        "scheduled": "✅⌚ Access Approved and Scheduled",
        "expired": "⏳ Access Request Expired",
        "ended": "🔒 Access Ended",
        "granted": "🔓 Access Granted",
        "approved": "✅ Access Request Approved",
        "rejected": "❌ Access Request Rejected",
        "revoked": "⛔ Access Revoked",
        "cancelled": "✖ Access Request Cancelled"
    }
    return titles.get(status, "ℹ️ Access Request Unhandled Exception")


def get_approver_mentions_from_status(status, approver_users):
    """
    # Modify here to conditionally include approver mentions
    """
    if status == "pending":
        approver_mentions = ", ".join([f"<at>{approver['UserName']}</at>" for approver in approver_users])
    else:
        # If not "pending", list approver names without mention or handle differently as needed
        approver_mentions = ", ".join([approver.get('Name', {}).get('Formatted', '') for approver in approver_users])
    return approver_mentions


def create_column_one(message_details, user, approver_mentions, approved_by=None, rejected_by=None, revoked_by=None):
    """
    Creates the first column for the AdaptiveCard based on message details,
    adjusting the approver/approved by/rejected by/revoked by fact based on the status.
    """
    # Initialize the items list with common elements
    items = [
        {
            "type": "FactSet",
            "facts": [
                {
                    "title": "Requestor:",
                    "value": f"<at>{user['UserName']}</at>"
                },
                {
                    "title": "Account:",
                    "value": f"{message_details.get('accountName', 'N/A')} ({message_details.get('accountId', 'N/A')})"
                }
            ]
        }
    ]

    # Insert the approver/approved by/rejected by fact
    if rejected_by:
        approver_fact = {
            "title": "Rejected By:",
            "value": rejected_by
        }
    elif revoked_by:
        approver_fact = {
            "title": "Revoked By:",
            "value": revoked_by
        }
    elif approved_by:
        approver_fact = {
            "title": "Approved By:",
            "value": approved_by
        }
    else:
        # If approved_by is not provided, show the approver mentions as before
        approver_fact = {
            "title": "Approvers:",
            "value": approver_mentions
        }

    # Insert the approver_fact into the items list at the desired position
    # Assuming it should come after the "Requestor:" entry
    items[0]["facts"].insert(1, approver_fact)

    # Define the column structure with the updated items list
    column = {
        "type": "Column",
        "width": "300px",
        "items": items
    }

    return column


def create_column_two(message_details):
    """
    Creates the second column for the AdaptiveCard based on message details.
    """
    column = {
        "type": "Column",
        "width": "auto",
        "items": [
            {
                "type": "FactSet",
                "facts": [
                    {
                        "title": "Role:",
                        "value": message_details.get('role', 'N/A')
                    },
                    {
                        "title": "Duration:",
                        "value": f"{message_details.get('time', 'N/A')} hours"
                    },
                    {
                        "title": "Justification:",
                        "value": message_details.get('justification', 'N/A')
                    }
                ]
            }
        ]
    }
    return column


def create_mentions(user, approver_users, status):
    """
    Creates the mention entities for the user and approvers based on the status.
    """
    mentions = [
        {
            "type": "mention",
            "text": f"<at>{user['UserName']}</at>",
            "mentioned": {
                "id": user['UserName'],
                "name": user.get('Name', {}).get('Formatted', '')
            }
        }
    ]

    if status == "pending":
        mentions += [
            {
                "type": "mention",
                "text": f"<at>{approver['UserName']}</at>",
                "mentioned": {
                    "id": approver['UserName'],
                    "name": approver.get('Name', {}).get('Formatted', '')
                }
            } for approver in approver_users
        ]

    return mentions


def send_teams_message(teams_message):
    """
    Sends the constructed message to Microsoft Teams.
    """
    webhook_url = os.getenv('TEAMS_WEBHOOK_URL')
    if not webhook_url:
        logger.error('TEAMS_WEBHOOK_URL environment variable is not set.')
        return {
            'statusCode': 400,
            'body': json.dumps('TEAMS_WEBHOOK_URL environment variable is not set.')
        }
    
    response = requests.post(webhook_url, json=teams_message, headers={"Content-Type": "application/json", "charset": "UTF-8"})
    if response.status_code == 200:
        logger.info('Message sent to Microsoft Teams successfully.')
        return {
            'statusCode': 200,
            'body': json.dumps('Message sent to Microsoft Teams successfully.')
        }
    else:
        logger.error(f"Failed to send message to Microsoft Teams. Response: {response.text}")
        return {
            'statusCode': response.status_code,
            'body': json.dumps(f"Failed to send message to Microsoft Teams. Response: {response.text}")
        }

