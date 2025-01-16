from classes.unisep_api import UniSepAPIHandler
from classes.runtime_tracker import RuntimeTracker
from classes.config_reader import ConfigReader


class Placeholder:
    def __init__(self):
        pass
    


if __name__ == '__main__':
    RuntimeTracker.start()
    web3_api = UniSepAPIHandler()
    config = ConfigReader()

    pool_address = config.get_section('uniswap-pools-sepolia')['weth-usdc']
    print(web3_api.get_pool_tokens(pool_address))


    RuntimeTracker.stop()