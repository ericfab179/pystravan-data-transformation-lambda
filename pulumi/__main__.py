"""An AWS Python Pulumi program"""

import os
import pulumi
import zipfile
import json
from datetime import datetime

import pulumi_aws as aws

def create_zip_from_folder(folder_path, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))



folder_path = '../cycling-data-transformation-lambda/.aws-sam/build/CyclingDataTransformationFunction'
zip_file_path = f'lambda_package_{str(int(datetime.now().timestamp()))}.zip'
function_name = 'cycling-data-transformation-data'
handler_name = 'handler.lambda_handler'
runtime = 'python3.8'

create_zip_from_folder(folder_path, zip_file_path)

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
            inline_policies=[
                aws.iam.RoleInlinePolicyArgs(
                    name="my_inline_policy",
                    policy="""{
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
                                    "arn:aws:s3:::pystravan-silver/*",
                                    "arn:aws:s3:::pystravan-gold/*"
                                ],
                                "Effect": "Allow"
                            }]
                        }""",
                )
            ]
        )


lambda_function = aws.lambda_.Function(
        function_name,
        role=lambda_iam_role.arn,
        code=zip_file_path,
        handler=handler_name,
        runtime=runtime,
        timeout=60
    )

# Export the function's ARN
pulumi.export('lambda_function_arn', lambda_function.arn)
