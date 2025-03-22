from classes.web3_client import Web3Client
from classes.runtime_tracker import RuntimeTracker
from classes.config_reader import ConfigReader


class Placeholder:
    def __init__(self):
        pass
    


if __name__ == '__main__':
    RuntimeTracker.start()
    w3 = Web3Client()
    config = ConfigReader()
    
    lp_proxy_address = config.get_value_checksum('mainnet-uniswap-pools', 'USDC_WETH')
    print(lp_proxy_address)
    print(w3.get_implementation_address())
    

    RuntimeTracker.stop()