# Use an official AWS Lambda runtime as a parent image
FROM public.ecr.aws/lambda/python:3.12

# Install dependencies
RUN pip install requests boto3>=1.34.42

# Copy all Python files in the directory
COPY temp-access-update-notifications/src/*.py ./

# Copy the common directory
COPY common/src/aws_utilities.py ./

# Set the CMD to your handler (app.lambda_handler)
CMD ["app.lambda_handler"]
