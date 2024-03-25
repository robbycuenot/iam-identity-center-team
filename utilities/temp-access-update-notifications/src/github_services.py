import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_latest_github_release_data(url):
    """
    Retrieves the latest release data from the GitHub API.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        latest_release = response.json()
        return latest_release
    except Exception as e:
        logger.error("Error querying GitHub API: %s", e)
        return None


def get_latest_github_release_notes(release_data):
    """
    Retrieves the release notes from the latest release data.
    """
    try:
        return release_data['body']
    except Exception as e:
        logger.error("Error getting GitHub release notes: %s", e)
        return None


def get_latest_github_release_version(release_data):
    """
    Retrieves the release version from the latest release data.
    """
    try:
        return release_data['tag_name']
    except Exception as e:
        logger.error("Error getting GitHub release version: %s", e)
        return None
