from classes.aws_client import AWSClient
from classes.config_reader import ConfigReader

from web3 import Web3



class Web3Client:
    def __init__(self):
        self.aws_api = AWSClient()
        self.credentials = self.aws_api.get_sepolia_credentials()
        self.provider_url = self.credentials['sepolia-endpoint']
        self.wallet_key = self.credentials['private-key']
        self.web3 = Web3(Web3.HTTPProvider(self.provider_url))
        self.token_addresses = self._get_token_addresses()

    def _get_token_addresses(self):
        config = ConfigReader()
        return config.get_section('token-addresses')

    # Wallet API calls
    def get_wallet_address(self):
        return self.web3.eth.account.from_key(self.wallet_key).address

    def get_wallet_balance(self, wallet_address):
        balance = self.web3.eth.get_balance(wallet_address)
        return self.web3.from_wei(balance, 'ether')

    def subscribe_new_blocks(self, process_block: Callable[[dict], None]):

        subscription = self.web3.eth.subscribe("newHeads")

        try:
            for new_block in subscription:
                # Convert block number from hex to int
                new_block["number"] = int(new_block["number"], 16)

                # Call the callback function with the block details
                process_block(new_block)

        except Exception as e:
            print(f"Error in block subscription: {e}")
            # Handle reconnection logic if needed
