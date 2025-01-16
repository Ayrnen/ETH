from classes.aws_api import AWSAPIHandler
from classes.etherscan_api import EtherscanAPIHandler
from classes.runtime_tracker import RuntimeTracker
from classes.config_reader import ConfigReader

from web3 import Web3



class UniSepAPIHandler:
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
        return config.get_section('token-addresses-sepolia')


    def get_wallet_address(self):
        return self.web3.eth.account.from_key(self.wallet_key).address

    def get_wallet_balance(self):
        wallet_address = self.get_wallet_address()
        balance = self.web3.eth.get_balance(wallet_address)
        return self.web3.from_wei(balance, 'ether')


    def create_liquidity_pool(self, token0, token1, fee, tick_lower, tick_upper):
        v3_factory_address = '0x0227628f3F023bb0B980b67D528571c95c6DaC1c'
        v3_factory_abi = self.etherscan.get_contract_abi(v3_factory_address)

        contract = self.web3.eth.contract(address=Web3.to_checksum_address(v3_factory_address), abi=v3_factory_abi)
        token0_sep = self.token_addresses[token0]
        token1_sep = self.token_addresses[token1]

        pool_address = contract.functions.createPool(token0_sep, token1_sep, fee, tick_lower, tick_upper).call()

        return pool_address

    def get_pool_slot0(self, pool_address):
        pool_abi = self.etherscan.get_contract_abi(pool_address)
        pool_contract = self.web3.eth.contract(address=Web3.to_checksum_address(pool_address), abi=pool_abi)

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

    def get_pool_liquidity(self, pool_address):
        pool_abi = self.etherscan.get_contract_abi(pool_address)
        pool_contract = self.web3.eth.contract(address=Web3.to_checksum_address(pool_address), abi=pool_abi)

        liquidity = pool_contract.functions.liquidity().call()
        return liquidity

    
    def get_pool_tokens(self, pool_address):
        pool_abi = self.etherscan.get_contract_abi(pool_address)
        pool_contract = self.web3.eth.contract(address=Web3.to_checksum_address(pool_address), abi=pool_abi)

        token0 = pool_contract.functions.token0().call()
        token1 = pool_contract.functions.token1().call()
        return {
            'token0': token0,
            'token1': token1
        }
    
    def get_pool_owner(self, pool_address):
        pool_abi = self.etherscan.get_contract_abi(pool_address)
        pool_contract = self.web3.eth.contract(address=Web3.to_checksum_address(pool_address), abi=pool_abi)

        owner = pool_contract.functions.owner().call()
        return owner