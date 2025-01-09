import requests
import json
import os
from dotenv import load_dotenv

class EtherscanAPIHandler:
    def __init__(self):
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        load_dotenv(env_path)

        self.api_url = 'https://api-sepolia.etherscan.io/api'
        self.api_key = os.getenv('ETHERSCAN_API_KEY')

    def get_contract_abi(self, contract_address):
        params = {
            'module': 'contract',
            'action': 'getabi',
            'address': contract_address,
            'apikey': self.api_key
        }

        # Make the API request
        response = requests.get(self.api_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == '1':
                return json.loads(data['result'])
            else:
                raise Exception(f'Error fetching ABI: {data['message']}')
        else:
            raise Exception(f'HTTP Error: {response.status_code}')