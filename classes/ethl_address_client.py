from classes.config_reader import ConfigReader
from classes.etherscan_client import EtherscanClient

import asyncio
import json
import requests
from web3 import Web3
from websockets import connect
import os

class ETHLAddressClient:
    def __init__(self, address):
        self.config = ConfigReader()
        self.etherscan = EtherscanClient('Mainnet')
        self.address = address

        self.api_key = os.getenv('INFURA_API_KEY')
        self.ws_url = 'wss://mainnet.infura.io/ws/v3/' + self.api_key
        self.http_url = 'https://mainnet.infura.io/v3/' + self.api_key
        self.web3 = Web3(Web3.HTTPProvider(self.http_url))
        if not self.web3.is_connected():
            raise ConnectionError('Failed to connect to Web3 provider')

        
    def get_balance_eth(self):
        balance = self.web3.eth.get_balance(self.address)
        return self.web3.from_wei(balance, 'ether')

    def get_balance_token(self, token_code):
        token_address = self.config.get_value('mainnet-token-addresses', token_code)
        return self.etherscan.get_balance_token(self.address, token_address)
        # def get_balance_token(self, token_code):
        #     token_address = self.config.get_value_checksum('mainnet-token-addresses', token_code)
        #     token_abi = self.etherscan.get_contract_abi(token_address)
        #     token_contract = self.web3.eth.contract(address=token_address, abi=token_abi)

        #     # print(token_contract.all_functions())

        #     implementation_address = token_contract.functions.implementation().call()
        #     implementation_abi = self.etherscan.get_contract_abi(implementation_address)
        #     implementation_contract = self.web3.eth.contract(address=implementation_address, abi=implementation_abi)
        #     balance = implementation_contract.balance_of(self.address).call()
        #     return balance

    def get_transaction_count(self):
        transactions = self.web3.eth.get_transaction_count(self.address)
        return transactions
    
    def get_lp_position(self, pair):
        lp_proxy_address = self.config.get_value_checksum('mainnet-uniswap-pools', pair)
        implementation_address = self.etherscan.get_implementation_address(lp_proxy_address)
        print(implementation_address)
        # lp_proxy_abi = self.etherscan.get_contract_abi(lp_proxy_address)
        # lp_proxy_contract = self.web3.eth.contract(address=lp_proxy_address, abi=lp_proxy_abi)

        # implementation_address = lp_proxy_contract.functions.implementation().call()
        # lp_abi = self.etherscan.get_contract_abi(implementation_address)
        # lp_contract = self.web3.eth.contract(address=implementation_address, abi=lp_abi)
        # print('contract success')

        # # Get token addresses from LP contract
        # token0_address = lp_contract.functions.token0().call()
        # token0_abi = self.etherscan.get_contract_abi(token0_address)
        # token1_address = lp_contract.functions.token1().call()
        # token1_abi = self.etherscan.get_contract_abi(token1_address)
        # print('token abis success')
        
        # # Setup token contracts
        # token0 = self.web3.eth.contract(address=token0_address, abi=token0_abi)
        # token1 = self.web3.eth.contract(address=token1_address, abi=token1_abi)
        
        # # Get token symbols
        # symbol0 = token0.functions.symbol().call()
        # symbol1 = token1.functions.symbol().call()
        
        # # Get token decimals
        # decimals0 = token0.functions.decimals().call()
        # decimals1 = token1.functions.decimals().call()
        
        # # Get LP decimals
        # lp_decimals = lp_contract.functions.decimals().call()
        
        # # Get user's LP balance and total supply
        # lp_balance = lp_contract.functions.balanceOf(self.address).call()
        # lp_total_supply = lp_contract.functions.totalSupply().call()
        
        # if lp_total_supply == 0:
        #     share = 0
        # else:
        #     share = lp_balance / lp_total_supply
        
        # # Get reserves
        # reserves = lp_contract.functions.getReserves().call()
        # reserve0, reserve1 = reserves[0], reserves[1]
        
        # # Calculate user's share of reserves
        # user_reserve0 = reserve0 * share
        # user_reserve1 = reserve1 * share
        
        # # Convert to human-readable amounts
        # user_amount0 = user_reserve0 / (10 ** decimals0)
        # user_amount1 = user_reserve1 / (10 ** decimals1)
        
        # # Format LP balance
        # formatted_lp_balance = lp_balance / (10 ** lp_decimals)
        
        # return {
        #     'lp_balance': formatted_lp_balance,
        #     'token0': {
        #         'address': token0_address,
        #         'symbol': symbol0,
        #         'amount': user_amount0,
        #         'decimals': decimals0
        #     },
        #     'token1': {
        #         'address': token1_address,
        #         'symbol': symbol1,
        #         'amount': user_amount1,
        #         'decimals': decimals1
        #     }
        # }


    async def get_pending_txns(self):
        async with connect(self.ws_url) as ws:
            await ws.send(json.dumps({
                'jsonrpc': '2.0',
                'id': 1,
                'method': 'eth_subscribe',
                'params': ['newPendingTransactions']
            }))
            # subscription_response = await ws.recv()

            while True:
                try:
                    message = await asyncio.wait_for(ws.recv(), timeout=15)
                    response = json.loads(message)
                    txHash = response['params']['result']
                    print(txHash)

                    tx = self.web3.eth.get_transaction(txHash)
                    if self.address == None:
                        message = await asyncio.wait_for(ws.recv(), timeout=15)
                        response = json.loads(message)
                        txHash = response['params']['result']
                        print(txHash)

                    elif tx.to == self.address:
                        print('Pending transaction found with the following details:')
                        print({
                            'hash': txHash,
                            'from': tx['from'],
                            'value': self.web3.fromWei(tx['value'], 'ether')
                        })

                except Exception as e:
                    print(f'An error occurred: {e}')
                    pass