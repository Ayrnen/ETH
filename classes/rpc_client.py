from web3 import Web3
from eth_abi.packed import encode_packed
from dotenv import load_dotenv
import os



class RPCClient:
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
    


        async def get_pending_txn(self, account_address=None):
        async with connect(self.ws_url) as ws:
            await ws.send(json.dumps({
                'jsonrpc': '2.0',
                'id': 1,
                'method': 'eth_subscribe',
                'params': ['newPendingTransactions']
            }))
            subscription_response = await ws.recv()
            print(f'Subscription Response:{subscription_response}')  # {'jsonrpc': '2.0', 'id': 1, 'result': '0xd67da23f62a01f58042bc73d3f1c8936'}

            while True:
                try:
                    message = await asyncio.wait_for(ws.recv(), timeout=15)
                    response = json.loads(message)
                    txHash = response['params']['result']
                    print(txHash)

                    tx = self.web3.eth.get_transaction(txHash)
                    if account_address == None:
                        message = await asyncio.wait_for(ws.recv(), timeout=15)
                        response = json.loads(message)
                        txHash = response['params']['result']
                        print(txHash)

                    elif tx.to == account_address:
                        print('Pending transaction found with the following details:')
                        print({
                            'hash': txHash,
                            'from': tx['from'],
                            'value': self.web3.fromWei(tx['value'], 'ether')
                        })

                except Exception as e:
                    print(f'An error occurred: {e}')
                    pass

    async def get_new_blocks(self):
        async with connect(self.ws_url) as ws:
            await ws.send(json.dumps({
                'jsonrpc': '2.0', 
                'id': 1, 
                'method': 'eth_subscribe', 
                'params': ['newHeads']
            }))
            subscription_response = await ws.recv()
            print(f'Subscription Response:{subscription_response}') 

            while True:
                try:
                    # Wait for new messages (new block headers)
                    message = await asyncio.wait_for(ws.recv(), timeout=15)
                    response = json.loads(message)
                    print(f'Response: {response["result"]}')
                    
                    # Extract block hash from the response
                    block_hash = response['params']['result']['hash']
                    
                    # Get the block details using the block hash
                    block = self.web3.eth.get_block(block_hash)
                    
                    # Print block number
                    print(f'New block mined: {block["number"]}')

                except asyncio.TimeoutError:
                    print('Connection timeout. Trying again...')
                except Exception as e:
                    print(f'An error occurred: {e}')
                    pass