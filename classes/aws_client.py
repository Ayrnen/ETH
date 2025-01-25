import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError
import json


class AWSClient:
    def __init__(self):
        load_dotenv()
        self.access_key = os.environ.get('ACCESS_KEY')
        self.secret_key = os.environ.get('SECRET_KEY')
        self.secret_name = os.environ.get('SECRET_NAME')
        self.region_name = os.environ.get('SECRET_REGION')

    def get_sepolia_credentials(self):
        session = boto3.session.Session()
        client = session.client(
            service_name = 'secretsmanager',
            aws_access_key_id = self.access_key,
            aws_secret_access_key = self.secret_key,
            region_name = self.region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=self.secret_name
            )
        except ClientError as e:
            raise e

        secret = get_secret_value_response['SecretString']

        return json.loads(secret)