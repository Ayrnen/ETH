import asyncio
import json
import requests
from web3 import Web3
from websockets import connect


class ETHLAddressClient:
    def __init__(self, address):
        self.ws_url = 'wss://mainnet.infura.io/ws/v3/990dd01e4e974b4ea477b0dbeeacb288'
        self.http_url = 'https://mainnet.infura.io/v3/990dd01e4e974b4ea477b0dbeeacb288'
        self.web3 = Web3(Web3.HTTPProvider(self.http_url))
        self.address = address
    

    