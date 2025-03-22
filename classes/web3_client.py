from classes.config_reader import ConfigReader

from web3 import Web3
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

    def _get_token_addresses(self):
        config = ConfigReader()
        return config.get_section('token-addresses')

    # Wallet API calls
    def get_wallet_address(self):
        return self.web3.eth.account.from_key(self.wallet_key).address

    def get_wallet_balance(self, wallet_address):
        balance = self.web3.eth.get_balance(wallet_address)
        return self.web3.from_wei(balance, 'ether')

    # def subscribe_new_blocks(self, process_block: Callable[[dict], None]):

    #     subscription = self.web3.eth.subscribe("newHeads")

    #     try:
    #         for new_block in subscription:
    #             # Convert block number from hex to int
    #             new_block["number"] = int(new_block["number"], 16)

    #             # Call the callback function with the block details
    #             process_block(new_block)

    #     except Exception as e:
    #         print(f"Error in block subscription: {e}")
    #         # Handle reconnection logic if needed

    def get_implementation_address(self, proxy_address):
        implementation_address = self.web3.eth.contract(address=proxy_address).functions.implementation().call()
        return implementation_address