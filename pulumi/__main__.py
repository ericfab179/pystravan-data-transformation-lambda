"""An AWS Python Pulumi program"""

import os
import pulumi
import zipfile

import pulumi_aws as aws

def create_zip_from_folder(folder_path, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

folder_path = '../cycling-data-transformation-lambda/.aws-sam/build/CyclingDataTransformationFunction'
zip_file_path = 'lambda_package.zip'
function_name = 'cycling-data-transformation-data'
handler_name = 'handler.lambda_handler'
runtime = 'python3.8'

lambda_iam_role = aws.iam.Role(function_name,
            assume_role_policy="""{
                "Version": "2012-10-17",
                "Statement": [{
                    "Action": "sts:AssumeRole",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    },
                    "Effect": "Allow",
                    "Sid": ""
                }]
            }""",
            inline_policies={
                "lambda_execution_policy": """{
                    "Version": "2012-10-17",
                    "Statement": [{
                        "Action": [
                            "logs:CreateLogGroup",
                            "logs:CreateLogStream",
                            "logs:PutLogEvents"
                        ],
                        "Resource": "arn:aws:logs:*:*:*",
                        "Effect": "Allow"
                    },
                    {
                        "Action": [
                            "s3:GetObject",
                            "s3:PutObject"
                        ],
                        "Resource": [
                            "arn:aws:s3:::your_source_bucket_nameCHANGE_ME/*",
                            "arn:aws:s3:::your_destination_bucket_nameCHANGE_ME/*"
                        ],
                        "Effect": "Allow"
                    }]
                }"""
            }
        )

lambda_function = aws.lambda_.Function(
        function_name,
        role=lambda_iam_role,
        code=aws.lambda_.Code.from_asset(zip_file_path),
        handler=handler_name,
        runtime=runtime
    )

# Export the function's ARN
pulumi.export('lambda_function_arn', lambda_function.arn)