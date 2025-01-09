from classes.aws_api import AWSAPIHandler
from classes.etherscan_api import EtherscanAPIHandler
from classes.runtime_tracker import RuntimeTracker
from web3 import Web3
import datetime as dt



class Sepolia:
    def __init__(self):
        self.aws_api = AWS_API()
        self.etherscan = EtherscanAPI()
        self.credentials = self.aws_api.get_sepolia_credentials()
        self.provider_url = self.credentials['sepolia-endpoint']
        self.wallet_key = self.credentials['private-key']
        self.web3 = Web3(Web3.HTTPProvider(self.provider_url))

        if self.web3.is_connected():
            print("Connected to Sepolia Testnet!")
        else:
            print("Failed to connect")

    def get_wallet_address(self):
        return self.web3.eth.account.from_key(self.wallet_key).address

    def get_wallet_balance(self):
        wallet_address = self.get_wallet_address()
        balance = self.web3.eth.get_balance(wallet_address)
        return self.web3.from_wei(balance, 'ether')


    def interact_with_factory(self):
        v3_factory_address = '0x0227628f3F023bb0B980b67D528571c95c6DaC1c'
        v3_factory_abi = self.etherscan.get_contract_abi(v3_factory_address)
        print('ABI Fetched!')

        contract = self.web3.eth.contract(address=Web3.to_checksum_address(v3_factory_address), abi=v3_factory_abi)
        print('Contract Created!')

        eth_sep = '0x7b79995e5f793A07Bc00c21412e50Ecae098E7f9'
        usdc_sep = '0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238'
        fee = 3000

        pool_address = contract.functions.getPool(eth_sep, usdc_sep, fee).call()
        print(f"Pool Address: {pool_address}")





if __name__ == '__main__':
    RuntimeTracker.start()
    sepolia = Sepolia()

    print(f'Wallet Address: {sepolia.get_wallet_address()}')
    print(f'Wallet Balance: {sepolia.get_wallet_balance()} ETH')

    sepolia.interact_with_factory()

    RuntimeTracker.stop()