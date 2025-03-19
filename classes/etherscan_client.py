import requests
import json
import os
from dotenv import load_dotenv

class EtherscanClient:
    def __init__(self, network):
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        load_dotenv(env_path)

        self.api_key = os.getenv('ETHERSCAN_API_KEY')

        if network == 'Mainnet': self.api_url = 'https://api.etherscan.io/api'
        elif network == 'Sepolia': self.api_url = 'https://api-sepolia.etherscan.io/api'

    def get_balance_token(self, wallet_address, token_address):
        params = {
            'module': 'account',
            'action': 'tokenbalance',
            'contractaddress': token_address,
            'address': wallet_address,
            'tag': 'latest',
            'apikey': self.api_key
        }

        response = requests.get(self.api_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        if data['status'] == '1':
            raw_balance = int(data['result'])
            decimals = self.get_token_decimals(token_address)
            return raw_balance / (10 ** decimals)
        else:
            raise Exception(f'Token Balance API Error: {data.get("message", "Unknown")}')

    def get_token_decimals(self, token_address):
        params = {
            'module': 'proxy',
            'action': 'eth_call',
            'to': token_address,
            'data': '0x313ce567',
            'apikey': self.api_key,
            'tag': 'latest',
        }
        response = requests.get(self.api_url, params=params)
        response.raise_for_status()
        data = response.json()
        return int(data['result'], 16) if data['result'] else 18




    def get_contract_abi(self, contract_address):
        params = {
            'module': 'contract',
            'action': 'getabi',
            'address': contract_address,
            'apikey': self.api_key,
            'tag': 'latest',
        }

        response = requests.get(self.api_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        if data['status'] == '1':
            return json.loads(data['result'])
        else:
            raise Exception(f'Contract ABI API Error: {data.get("message", "Unknown")}')