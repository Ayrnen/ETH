from web3 import Web3
from eth_abi.packed import encode_packed
from dotenv import load_dotenv
import os



class Web3Client:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('INFURA_API_KEY')
        self.ws_url = 'wss://mainnet.infura.io/ws/v3/' + self.api_key
        self.http_url = 'https://mainnet.infura.io/v3/' + self.api_key
        self.web3 = Web3(Web3.HTTPProvider(self.http_url))
        if not self.web3.is_connected():
            raise ConnectionError('Failed to connect to Web3 provider')

    def get_address_from_secret(self, secret):
        return self.web3.eth.account.from_key(secret).address

    def get_address_from_ens(self, ens_name):
        return self.web3.ens.address(ens_name)

    def get_balance_eth(self, address):
        balance = self.web3.eth.get_balance(address)
        return self.web3.from_wei(balance, 'ether')
    
    def get_transaction_count(self, address):
        return self.web3.eth.get_transaction_count(address)

    def get_position_key(self, address, tick_lower=-887272, tick_upper=887272):
        encoded_data = encode_packed(
            ['address', 'int24', 'int24'],
            [Web3.to_checksum_address(address), tick_lower, tick_upper]
        )
        return Web3.keccak(encoded_data)