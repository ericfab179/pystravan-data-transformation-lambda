import boto3
import pandas as pd
import io

def lambda_handler(event, context):
    """
    Powered by Chat GPT
    """
    # Set up the S3 client
    s3 = boto3.client('s3')

    # Retrieve the bucket and file names from the event
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    source_key = event['Records'][0]['s3']['object']['key']
    destination_bucket = 'pystravan-gold'
    destination_key = 'data.csv'

    # Read the CSV file from the source S3 bucket
    response = s3.get_object(Bucket=source_bucket, Key=source_key)
    csv_content = response['Body'].read().decode('utf-8')

    # Modify the CSV file
    modified_csv_content = transformations(csv_content)

    # Upload the modified CSV file to the destination S3 bucket
    s3.put_object(Body=modified_csv_content.encode('utf-8'), Bucket=destination_bucket, Key=destination_key, ACL='public-read')

    return {
        'statusCode': 200,
        'body': 'Modified CSV file uploaded successfully'
    }

def transformations(csv_content):

    data = pd.read_csv(io.StringIO(csv_content), skiprows=2)

    data['Total'] = data['Total'].str.replace(',','.').astype(float)

    # Convert the modified DataFrame back to CSV
    modified_csv_content = data.to_csv(index=False)

    return modified_csv_content
