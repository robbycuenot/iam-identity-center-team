import boto3
import logging
import os
import re

# Get the AWS region from environment variables; default to 'us-east-1' if not set
region = os.getenv('AWS_REGION', 'us-east-1')

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_amplify_app_id_from_name(app_name):
    """
    Retrieves the Amplify app ID for the given app name.
    """
    amplify_client = boto3.client('amplify', region_name=region)
    apps = amplify_client.list_apps()
    app = next((app for app in apps['apps'] if app['name'] == app_name), None)
    return app['appId'] if app else None


def get_amplify_team_admin_group_from_id(app_id):
    """
    Retrieves the admin group name from the Amplify app environment variables.
    """
    amplify_client = boto3.client('amplify', region_name=region)
    branch = amplify_client.get_branch(appId=app_id, branchName='main')
    env_variables = branch['branch']['environmentVariables']
    return env_variables['TEAM_ADMIN_GROUP']


def get_codecommit_app_latest_version_from_file(file_content):
    """
    Retrieves the version number from the file content.
    """
    # Regex to find the version number
    version_pattern = re.compile(r'https://github\.com/aws-samples/iam-identity-center-team/releases/tag/(v[0-9]+\.[0-9]+\.[0-9]+)')
    match = version_pattern.search(file_content)
    if match:
        return match.group(1)  # Returns the first capturing group (version number)
    else:
        return "Version not found"


def get_codecommit_file(repository_name, file_path):
    """
    Retrieves the file content from the default branch of the CodeCommit repository.
    """
    codecommit = boto3.client('codecommit', region_name=region)
    try:
        # Get the default branch name
        response = codecommit.get_repository(repositoryName=repository_name)
        default_branch = response['repositoryMetadata']['defaultBranch']

        # Get the file content from the default branch
        file_content_response = codecommit.get_file(
            repositoryName=repository_name,
            filePath=file_path,
            commitSpecifier=default_branch  # Optional: Specify a commit ID or branch name here
        )
        return file_content_response['fileContent'].decode('utf-8')
    except Exception as e:
        logger.error("Error getting file content: %s", e)
        return None


def get_group_members_from_group_id(identitystoreid, groupid):
    """
    Retrieves the members of a group from the Identity Store.
    """
    identitystore_client = boto3.client('identitystore', region_name=region)
    group_members_response = identitystore_client.list_group_memberships(
        IdentityStoreId=identitystoreid,
        GroupId=groupid
    )
    return group_members_response


def get_group_id_from_name(identitystoreid, groupname):
    """
    Retrieves the group ID from the Identity Store using the group name.
    """
    identitystore_client = boto3.client('identitystore', region_name=region)
    groups_response = identitystore_client.get_group_id(
        IdentityStoreId=identitystoreid,
        AlternateIdentifier={
            'UniqueAttribute': {
                'AttributePath': 'displayName',
                'AttributeValue': groupname
            }
        }
    )
    return groups_response['GroupId']


def get_identitystoreid():
    """
    Retrieves the Identity Store ID for a given SSO instance ARN.
    """
    sso_admin_client = boto3.client('sso-admin', region_name=region)
    sso_admin_instances = sso_admin_client.list_instances()
    sso_admin_instance = sso_admin_instances['Instances'][0]  # Assuming only one instance
    return sso_admin_instance['IdentityStoreId']


def get_user_from_email(identitystoreid, email):
    """
    Retrieves a user's details from the Identity Store using their email.
    """
    identitystore_client = boto3.client('identitystore', region_name=region)
    user_id_response = identitystore_client.get_user_id(
        IdentityStoreId=identitystoreid,
        AlternateIdentifier={
            'UniqueAttribute': {
                'AttributePath': 'emails.value',
                'AttributeValue': email
            }
        }
    )
    user_response = get_user_from_user_id(identitystoreid, user_id_response['UserId'])
    return user_response


def get_user_from_upn(identitystoreid, upn):
    """
    Retrieves a user's details from the Identity Store using their user principal name (UPN).
    """
    identitystore_client = boto3.client('identitystore', region_name=region)
    user_id_response = identitystore_client.get_user_id(
        IdentityStoreId=identitystoreid,
        AlternateIdentifier={
            'UniqueAttribute': {
                'AttributePath': 'userName',
                'AttributeValue': upn
            }
        }
    )
    user_response = get_user_from_user_id(identitystoreid, user_id_response['UserId'])
    return user_response


def get_user_from_user_id(identitystoreid, user_id):
    """
    Retrieves a user's details from the Identity Store using their email.
    """
    identitystore_client = boto3.client('identitystore', region_name=region)
    user_response = identitystore_client.describe_user(
        IdentityStoreId=identitystoreid,
        UserId=user_id
    )
    return user_response
