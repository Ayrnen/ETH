from classes.web3_api import Web3APIHandler
from classes.runtime_tracker import RuntimeTracker
from classes.config_reader import ConfigReader


class PoolValidator:
    def __init__(self):
        self.web3_api = Web3APIHandler()
        self.config = ConfigReader()
        self.factory_contract = self._get_factory_contract()

    def _get_factory_contract(self):
        factory_address = self.config.get_section('uniswap-factories')['v3']
        factory_contract = self.web3_api.get_factory_contract(factory_address)
        return factory_contract
    
    def get_pool_address(self, token0, token1, fee_tier):
        token0_address = self.web3_api.token_addresses[token0]
        token1_address = self.web3_api.token_addresses[token1]
        pool_address = self.web3_api.get_pool_address(self.factory_contract, token0_address, token1_address, fee_tier)
        return pool_address

    def validate_pool_existence(self, token0, token1, fee_tier):
        pool_address = self.get_pool_address(token0, token1, fee_tier)
        if pool_address == '0x0000000000000000000000000000000000000000':
            return False
        return True




if __name__ == '__main__':
    RuntimeTracker.start()
    pool_validator = PoolValidator()

    print(pool_validator.validate_pool_existence('usdc', 'weth', 3000))
    print(pool_validator.validate_pool_existence('usdt', 'weth', 3000))

    print('Validate USDC/WETH pool metadata:')
    pool_address = pool_validator.get_pool_address('usdt', 'weth', 3000)
    pool_contract = pool_validator.web3_api.get_pool_contract(pool_address)
    print('Pool Address:', pool_address)
    print('Slot 0:', pool_validator.web3_api.get_pool_slot0(pool_contract))
    print('Liquidity:', pool_validator.web3_api.get_pool_liquidity(pool_contract))
    print('Ticks:', pool_validator.web3_api.get_pool_ticks(pool_contract))
    


    RuntimeTracker.stop()