from classes.web3_client import Web3Client
from classes.runtime_tracker import RuntimeTracker
from classes.config_reader import ConfigReader
from classes.ethl_address_client import ETHLAddressClient
from classes.abi_reader import ABIReader


class Placeholder:
    def __init__(self):
        pass
    


if __name__ == '__main__':
    RuntimeTracker.start()

    # w3 = Web3Client()
    # address = w3.get_address_from_ens('vitalik.eth')


    address = '0x290ca4DA2c963deA5AE736469a5B8a53d64d4E6A'
    config = ConfigReader()
    lp_address = config.get_value_checksum('mainnet-uniswap-pools', 'USDT_WETH')

    abi_reader = ABIReader('uniswap')
    lp_abi = abi_reader.get_abi_by_address(lp_address)


    address_client = ETHLAddressClient(address)
    position = address_client.get_lp_position(lp_address, lp_abi)
    print(position)
    
    RuntimeTracker.stop()