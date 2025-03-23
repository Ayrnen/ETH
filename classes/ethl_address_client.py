from classes.config_reader import ConfigReader
from classes.etherscan_client import EtherscanClient
from classes.web3_client import Web3Client

import asyncio
import json
from websockets import connect

class ETHLAddressClient:
    def __init__(self, address):
        self.config = ConfigReader()
        self.etherscan = EtherscanClient('Mainnet')
        self.web3_client = Web3Client()
        self.address = address
        
    def get_balance_eth(self):
        return self.web3_client.get_balance_eth(self.address)
    
    def get_balance_token(self, token_address):
        return self.etherscan.get_balance_token(self.address, token_address)

    def get_transaction_count(self):
        return self.web3_client.get_transaction_count(self.address)    
    
    def get_lp_position(self, lp_address, lp_abi):
        position_key = self.web3_client.get_position_key(self.address)
        print(position_key)
        lp_contract = self.web3_client.web3.eth.contract(address=lp_address, abi=lp_abi)
        print(lp_contract)
        position_data = lp_contract.functions.positions(position_key).call()
        return position_data

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