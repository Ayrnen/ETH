from classes.web3_client import Web3Client
from classes.runtime_tracker import RuntimeTracker
from classes.config_reader import ConfigReader
from classes.ethl_address_client import ETHLAddressClient
from classes.abi_reader import ABIReader

from dotenv import load_dotenv
import os

class Placeholder:
    def __init__(self):
        pass
    


if __name__ == '__main__':
    RuntimeTracker.start()


    load_dotenv()
    w3 = Web3Client()
    ens_name = os.getenv('ENS_NAME')
    address = w3.get_address_from_ens(ens_name)

    config = ConfigReader()
    lp_address = config.get_value_checksum('mainnet-uniswap-pools', 'USDT_WETH')

    abi_reader = ABIReader('uniswap')
    lp_abi = abi_reader.get_abi_by_address(lp_address)


    address_client = ETHLAddressClient(address)
    position = address_client.get_lp_position(lp_address, lp_abi)
    print(position)
    
    RuntimeTracker.stop()