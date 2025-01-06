from classes.aws_access import AWSAccess
import json
from web3 import Web3

aws_access = AWSAccess()
credentials = aws_access.get_sepolia_credentials()
provider_url = credentials['sepolia-endpoint']
wallet_key = credentials['private-key']

web3 = Web3(Web3.HTTPProvider(provider_url))

if web3.is_connected():
    print("Connected to Sepolia Testnet!")
else:
    print("Failed to connect")