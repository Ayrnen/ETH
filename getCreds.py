import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError
import datetime as dt


class CredCollector:
    def __init__(self):
        load_dotenv()
        self.access_key = os.environ.get('ACCESS_KEY')
        self.secret_key = os.environ.get('SECRET_KEY')
        self.secret_name = os.environ.get('SECRET_NAME')
        self.region_name = os.environ.get('SECRET_REGION')

    def get_credentials(self):
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

        return secret
    
    # @staticmethod
    # def csv_filename(name):
    #     today = dt.datetime.now().strftime('%Y-%m-%d')
    #     return f'/CSV_Files/{name}_{today}.csv'

    # @staticmethod
    # def save_data(data, filename):
    #     data.to_csv(filename, index=False)


# Fetch data
if __name__ == '__main__':
    collector = CredCollector()
    start_time = dt.datetime.now()

    print(collector.get_credentials())
    print(type(collector.get_credentials()))

    # end_time = dt.datetime.now()
    # print(f'Runtime: {end_time - start_time}')
    # print('Data Collection Complete')