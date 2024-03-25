# Use the latest Microsoft universal image for Codespaces
FROM mcr.microsoft.com/devcontainers/universal:latest

# Install the AWS CLI v2
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends curl unzip \
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    # Clean up unnecessary files
    && rm -rf awscliv2.zip ./aws \
    # Enable AWS CLI autocompletion in Bash
    && echo "complete -C '/usr/local/bin/aws_completer' aws" >> /home/codespace/.bashrc \
    && echo "complete -C '/usr/local/bin/aws_completer' aws" >> /home/codespace/.profile

# Update pip and install git-remote-codecommit
RUN pip3 install --upgrade pip && pip3 install git-remote-codecommit boto3>=1.34.42

# Create an aws configuration file with named profiles for the TEAM account and Management account in /home/codespace/.aws
RUN mkdir -p /home/codespace/.aws && \
    echo "[profile team_account_profile]" > /home/codespace/.aws/config && \
    echo "aws_access_key_id = <team_account_access_key_id>" >> /home/codespace/.aws/config && \
    echo "aws_secret_access_key = <team_account_secret_access_key>" >> /home/codespace/.aws/config && \
    echo "aws_session_token = <team_account_session_token>" >> /home/codespace/.aws/config && \
    echo "region = us-east-1" >> /home/codespace/.aws/config && \
    echo "output = json" >> /home/codespace/.aws/config && \
    echo "" >> /home/codespace/.aws/config && \
    echo "[profile org_master_profile]" >> /home/codespace/.aws/config && \
    echo "aws_access_key_id = <org_master_access_key_id>" >> /home/codespace/.aws/config && \
    echo "aws_secret_access_key = <org_master_secret_access_key>" >> /home/codespace/.aws/config && \
    echo "aws_session_token = <org_master_session_token>" >> /home/codespace/.aws/config && \
    echo "region = us-east-1" >> /home/codespace/.aws/config && \
    echo "output = json" >> /home/codespace/.aws/config

# Install Terraform CLI
RUN curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add - \
    && sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main" \
    && sudo apt-get update && sudo apt-get install terraform

# Add an alias for 'tf' to call 'terraform' and set ownership to the codespace user
RUN echo 'alias tf="terraform"' >> /home/codespace/.bashrc \
    && echo 'alias tf="terraform"' >> /home/codespace/.profile

# Add aliases for local testing
RUN echo 'alias start_notifications="./utilities/ms-teams-notifications/tests/start_notifications.sh"' >> /home/codespace/.bashrc \
    && echo 'alias start_notifications="./utilities/ms-teams-notifications/tests/start_notifications.sh"' >> /home/codespace/.profile \
    && echo 'alias test_notifications="./utilities/ms-teams-notifications/tests/test_notifications.sh"' >> /home/codespace/.bashrc \
    && echo 'alias test_notifications="./utilities/ms-teams-notifications/tests/test_notifications.sh"' >> /home/codespace/.profile \
    && echo 'alias test_update_notifications="./utilities/temp-access-update-notifications/tests/test_update_notifications.sh"' >> /home/codespace/.bashrc \
    && echo 'alias test_update_notifications="./utilities/temp-access-update-notifications/tests/test_update_notifications.sh"' >> /home/codespace/.profile

# Change ownership to the codespace user
RUN chown codespace:codespace /home/codespace/.bashrc \
    && chown codespace:codespace /home/codespace/.profile \
    && chown -R codespace:codespace /home/codespace/.aws
