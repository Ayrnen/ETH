from classes.web3_api import Web3APIHandler
from classes.runtime_tracker import RuntimeTracker
from classes.config_reader import ConfigReader


class Placeholder:
    def __init__(self):
        pass
    


if __name__ == '__main__':
    RuntimeTracker.start()
    web3_api = Web3APIHandler()
    config = ConfigReader()


    factory_address = config.get_section('uniswap-factories')['v3']
    factory_contract = web3_api.get_factory_contract(factory_address)

    
    pool_fee = int(config.get_section('uniswap-pools')['usdc-weth-fee'])
    print(web3_api.get_pool_address(factory_contract, web3_api.token_addresses['usdc'], web3_api.token_addresses['weth'], 3000))

    pool_fee = int(config.get_section('uniswap-pools')['usdt-weth-fee'])
    print(web3_api.get_pool_address(factory_contract, web3_api.token_addresses['usdt'], web3_api.token_addresses['weth'], 5000))

    pool_address = config.get_section('uniswap-pools')['usdc-weth']
    pool_contract = web3_api.get_pool_contract(pool_address)
    web3_api.get_pool_slot0(pool_contract, pool_address)
    # print(web3_api.get_pool_tokens(pool_address))

    web3_api.get_pool_slot0_old(pool_address)
    
    # pool_address = config.get_section('uniswap-pools')['usdt-weth']
    # print(web3_api.get_pool_tokens(pool_address))

    # web3_api.get_pool_slot0(factory_contract, pool_address)

    RuntimeTracker.stop()