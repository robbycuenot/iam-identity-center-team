import requests
import logging

# You might need this if you're logging within this file
logger = logging.getLogger()
logger.setLevel(logging.INFO)

github_release_url = "https://github.com/aws-samples/iam-identity-center-team/releases/tag/"

def construct_teams_message(github_version, codecommit_version, release_notes, notification_recipient_details, github_release_url):
    """
    Constructs the Adaptive Card payload for Microsoft Teams based on the new GitHub release.
    """
    adaptive_card = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "body": [
                        create_text_block("🌟 New Version Available"),
                        create_text_block("A new version has been released on GitHub."),
                        create_fact_set(
                            github_version, 
                            codecommit_version, 
                            release_notes, 
                            notification_recipient_details, 
                            github_release_url
                        )
                    ],
                    "msteams": {
                        "width": "Full",
                        "entities": create_mentions(notification_recipient_details)
                    }
                }
            }
        ]
    }
    return adaptive_card


def create_fact_set(github_version, codecommit_version, release_notes, notification_recipient_details, github_release_url):
    """
    Creates a fact set for the Adaptive Card.
    """
    facts = [
        {
            "title": "Attention:",
            "value": ", ".join([f"<at>{recipient['user_upn']}</at>" for recipient in notification_recipient_details])
        },
        {
            "title": "GitHub Version:",
            "value": f"[{github_version}]({github_release_url}{github_version})"
        },
        {
            "title": "Current Version:",
            "value": f"[{codecommit_version}]({github_release_url}{codecommit_version})"
        },
        {
            "title": "Release Notes:",
            "value": release_notes
        }
    ]
    return {"type": "FactSet", "facts": facts}


def create_mentions(notification_recipient_details):
    """
    Prepares mention entities for the Adaptive Card.
    """
    mentions = [
        {
            "type": "mention",
            "text": f"<at>{recipient['user_upn']}</at>",
            "mentioned": {
                "id": recipient['user_upn'],
                "name": recipient['user_name']
            }
        } for recipient in notification_recipient_details
    ]
    return mentions


def create_text_block(text, size="Medium", weight="Bolder", wrap=True):
    """
    Creates a text block for the Adaptive Card.
    """
    return {
        "type": "TextBlock",
        "size": size,
        "weight": weight,
        "text": text,
        "wrap": wrap
    }


def send_teams_message(teams_message, webhook_url):
    """
    Sends the constructed message to Microsoft Teams.
    """
    response = requests.post(webhook_url, json=teams_message, headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        logger.info('Message sent to Microsoft Teams successfully.')
    else:
        logger.error(f"Failed to send message to Microsoft Teams. Response: {response.text}")
