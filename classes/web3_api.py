from classes.aws_api import AWSAPIHandler
from classes.etherscan_api import EtherscanAPIHandler
from classes.runtime_tracker import RuntimeTracker
from classes.config_reader import ConfigReader

from web3 import Web3



class Web3APIHandler:
    def __init__(self):
        self.aws_api = AWSAPIHandler()
        self.etherscan = EtherscanAPIHandler()
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

    def get_wallet_balance(self):
        wallet_address = self.get_wallet_address()
        balance = self.web3.eth.get_balance(wallet_address)
        return self.web3.from_wei(balance, 'ether')



    # UniSwap API calls
    def get_factory_contract(self, factory_address):
        factory_abi = self.etherscan.get_contract_abi(factory_address)
        factory_contract = self.web3.eth.contract(address=Web3.to_checksum_address(factory_address), abi=factory_abi)
        return factory_contract

    def get_pool_address(self, factory_contract, token0, token1, fee_tier):
        pool_address = factory_contract.functions.getPool(
            Web3.to_checksum_address(token0),
            Web3.to_checksum_address(token1),
            fee_tier
        ).call()
        return pool_address
    
    def get_pool_tokens(self, pool_address):
        pool_abi = self.etherscan.get_contract_abi(pool_address)
        pool_contract = self.web3.eth.contract(address=Web3.to_checksum_address(pool_address), abi=pool_abi)
        token0 = pool_contract.functions.token0().call()
        token1 = pool_contract.functions.token1().call()

        return {'token0': token0, 'token1': token1}

    def create_pool(self, factory_contract, token0, token1, fee, tick_lower, tick_upper):
        token0_address = self.token_addresses[token0]
        token1_address = self.token_addresses[token1]
        pool_address = factory_contract.functions.createPool(token0_address, token1_address, fee, tick_lower, tick_upper).call()
        return pool_address


    def get_pool_contract(self, pool_address):
        pool_abi = self.etherscan.get_contract_abi(pool_address)
        pool_contract = self.web3.eth.contract(address=Web3.to_checksum_address(pool_address), abi=pool_abi)
        return pool_contract


    def get_pool_slot0(self, pool_contract, pool_address):
        print(pool_contract.functions.slot0().call())

    def get_pool_slot0_old(self, s):
            pool_abi = self.etherscan.get_contract_abi(pool_address)
            pool_contract = self.web3.eth.contract(address=Web3.to_ch ecksum_address(pool_address), abi=pool_abi)

            slot0 = pool_contract.functions.slot0().call()
            
            return {
                'price': (slot0[0] / (2 ** 96)) ** 2,
                'tick_index': slot0[1],
                'obs_idx': slot0[2],
                'obs_cardinality': slot0[3],
                'obs_cardinality_next': slot0[4],
                'fee_protocol': slot0[5],
                'lock_status': slot0[6]
            }
        
