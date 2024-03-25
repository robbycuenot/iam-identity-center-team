import json
import logging
import os

from aws_utilities import (
    get_amplify_app_id_from_name,
    get_amplify_team_admin_group_from_id,
    get_codecommit_app_latest_version_from_file,
    get_codecommit_file,
    get_group_id_from_name,
    get_group_members_from_group_id,
    get_identitystoreid,
    get_user_from_email,
    get_user_from_upn,
    get_user_from_user_id
)
from github_services import (
    get_latest_github_release_data,
    get_latest_github_release_notes,
    get_latest_github_release_version
)
from teams_communication import (
    construct_teams_message,
    send_teams_message
)

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Environment variables
region = os.getenv('AWS_REGION', 'us-east-1')
repository_name = 'team-idc-app'
app_name = 'TEAM-IDC-APP'
file_path = 'src/components/Navigation/Header.js'
github_repo_url = 'https://api.github.com/repos/aws-samples/iam-identity-center-team/releases/latest'
github_release_url = "https://github.com/aws-samples/iam-identity-center-team/releases/tag/"

def lambda_handler(event, context):
    # Log the received event
    logger.info("Received event: %s", json.dumps(event))

    # Get the latest GitHub release version
    github_release_data = get_latest_github_release_data(github_repo_url)
    github_version = get_latest_github_release_version(github_release_data)
    if github_version:
        logger.info("Latest GitHub Release Version: %s", github_version)
    else:
        logger.error("Failed to get the latest GitHub release version.")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error getting the latest GitHub release version'})
        }

    # Get the latest file version from CodeCommit
    file_content = get_codecommit_file(repository_name, file_path)
    if file_content:
        codecommit_version = get_codecommit_app_latest_version_from_file(file_content)
        logger.info("Extracted Version from CodeCommit: %s", codecommit_version)
    else:
        logger.error("Failed to get file content from CodeCommit.")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error getting file content from CodeCommit'})
        }

    # Compare GitHub and CodeCommit versions
    # If the versions are different, log the details and send a notification
    # If the versions are the same, log the details and return a success response
    if github_version != codecommit_version:
        logger.info("New version on GitHub: %s. Current version in CodeCommit: %s.", github_version, codecommit_version)
        
        # Notification recepients can be determined using several methods, which are hierarchical in nature:
            # If no UPDATE_NOTIFICATION* environment variables are set, the Amplify app environment variables are used
            # If the UPDATE_NOTIFICATION_GROUP environment variable is set, the group members are retrieved and used instead
            # If the UPDATE_NOTIFICATION_USER_EMAIL environment variable is set, the user details are retrieved and used instead
            # The hierarchy is as follows:
                # UPDATE_NOTIFICATION_USER_EMAIL > UPDATE_NOTIFICATION_GROUP > Amplify app environment variables
                # Please keep this in mind, as only the highest precedence method will be used, and the others will be ignored
                # Specifying both UPDATE_NOTIFICATION_GROUP and UPDATE_NOTIFICATION_USER_EMAIL will favor the latter
        
        # Get the identity store ID to query user and group details
        identitystoreid = get_identitystoreid()
        
        # Array to store the details of the notification recepients
        notification_recipient_details = []

        # Get the UPDATE_NOTIFICATION_GROUP and UPDATE_NOTIFICATION_USER_EMAIL environment variables
        update_notification_group = os.getenv('UPDATE_NOTIFICATION_GROUP')
        update_notification_user_email = os.getenv('UPDATE_NOTIFICATION_USER_EMAIL')

        # If the UPDATE_NOTIFICATION_GROUP and UPDATE_NOTIFICATION_USER_EMAIL environment variables are not set,
        # retrieve the TEAM Admin Group from the Amplify app environment variables and use it as the notification group
        if not update_notification_group and not update_notification_user_email:
            app_id = get_amplify_app_id_from_name(app_name)
            update_notification_group = get_amplify_team_admin_group_from_id(app_id)
            logger.info("Using Amplify app environment variables to determine the notification group: %s", update_notification_group)

        # If the UPDATE_NOTIFICATION_USER_EMAIL environment variable is not set, it means we are using a group
        # Retrieve the group members and add them to the notification_recipient_details array
        if not update_notification_user_email:
            update_notification_group_id = get_group_id_from_name(identitystoreid, update_notification_group)
            group_members = get_group_members_from_group_id(identitystoreid, update_notification_group_id)

            for member in group_members['GroupMemberships']:
                user = get_user_from_user_id(identitystoreid, member['MemberId']['UserId'])
                user_upn = user['UserName']
                user_name = user['Name']['Formatted']
                notification_recipient_details.append({'user_upn': user_upn, 'user_name': user_name})
        
        # Otherwise, retrieve the user details based on the UPDATE_NOTIFICATION_USER_EMAIL environment variable
        else:
            try:
                # Attempt to retrieve the user details using the email address
                user = get_user_from_email(identitystoreid, update_notification_user_email)
            except Exception as e:
                logger.error(f"Failed to find user by email {update_notification_user_email}: {e}")
                try:
                    # If the above fails, attempt to retrieve the user details using the UPN
                    user = get_user_from_upn(identitystoreid, update_notification_user_email)
                except Exception as e:
                    logger.error(f"Failed to find user by UPN {update_notification_user_email}: {e}")
                    # If both attempts fail, log and raise an error
                    raise Exception(f"No user found with email or UPN {update_notification_user_email}")

            # If a user is found, extract the necessary details
            user_upn = user['UserName']
            user_name = user['Name']['Formatted']
            notification_recipient_details.append({'user_upn': user_upn, 'user_name': user_name})

        # Construct and send the Teams message
        release_notes = get_latest_github_release_notes(github_release_data)
        teams_message = construct_teams_message(github_version, codecommit_version, release_notes, notification_recipient_details, github_release_url)
        teams_webhook_url = os.getenv('TEAMS_WEBHOOK_URL')
        send_teams_message(teams_message, teams_webhook_url)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'New version detected on GitHub. Notification sent to Microsoft Teams.',
                'github_version': github_version,
                'codecommit_version': codecommit_version
            })
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Versions are up to date. No new version detected on GitHub.',
                'github_version': github_version,
                'codecommit_version': codecommit_version
            })
        }

if __name__ == "__main__":
    # This allows the file to be executed as a script for testing
    lambda_handler({}, {})
