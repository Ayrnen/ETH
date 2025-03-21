import requests
import json
import os
from dotenv import load_dotenv

class EtherscanClient:
    def __init__(self, network):
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        load_dotenv(env_path)

        self.api_key = os.getenv('ETHERSCAN_API_KEY')

        if network == 'Mainnet': self.url = 'https://api.etherscan.io/api'
        elif network == 'Sepolia': self.url = 'https://api-sepolia.etherscan.io/api'

    def get_balance_token(self, wallet_address, token_address):
        params = {
            'module': 'account',
            'action': 'tokenbalance',
            'contractaddress': token_address,
            'address': wallet_address,
            'tag': 'latest',
            'apikey': self.api_key
        }

        response = requests.get(self.url, params=params)
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
        response = requests.get(self.url, params=params)
        response.raise_for_status()
        data = response.json()
        return int(data['result'], 16) if data['result'] else 18




    def get_contract_abi(self, contract_address):
        params = {
            'module': 'contract',
            'action': 'getabi',
            'address': contract_address,
            'apikey': self.api_key
        }

        try:
            response = requests.get(self.url, params=params, timeout=10)  # Add timeout
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Request failed: {e}") from e
        
        data = response.json()
        if data['status'] == '1':
            try:
                return json.loads(data['result'])
            except json.JSONDecodeError:
                # This should never happen for verified contracts, but handle it anyway
                raise ValueError("ABI data corrupted") from None
        else:
            # Extract the specific error reason from 'result'
            error_message = data.get('result', 'Unknown error')
            if "not verified" in error_message:
                raise ValueError(f"Contract {contract_address} is not verified on Etherscan") from None
            else:
                raise Exception(f"Etherscan API Error: {error_message}")
        
    def get_implementation_address(self, proxy_address):
        params = {
            'module': 'contract',
            'action': 'getsourcecode',
            'address': proxy_address,
            'apikey': self.api_key
        }
        

        response = requests.get(self.url, params=params, timeout=10)
        data = response.json()
        print('Data:', data)
        if data['status'] == '1':
            implementation = data['result'][0].get('ImplementationAddress')
            if implementation:
                return implementation