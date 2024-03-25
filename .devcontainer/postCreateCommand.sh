#!/bin/bash
# postCreateCommand.sh

# Only proceed if AWS_REGION is set and not empty
if [ ! -z "$1" ]; then
    AWS_REGION_VALUE="$1"
    
    # Use sed to find "region = us-east-1" and replace it with "region = <AWS_REGION_VALUE>"
    sed -i "s/region = us-east-1/region = ${AWS_REGION_VALUE}/" /home/codespace/.aws/config
fi
