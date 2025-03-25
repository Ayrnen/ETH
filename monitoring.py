import time
import math
from datetime import datetime

from classes.config_reader import ConfigReader
from classes.rpc_client import RPCClient
from classes.aws_client import AWSClient
from classes.uniswap_client import UniswapClient
from classes.runtime_tracker import RuntimeTracker



class PoolMonitor:
    def __init__(self):
        self.web3_client = RPCClient()
        self.uniswap_client = UniswapClient()
        self.config = ConfigReader()
        self.factory_contract = self._get_factory_contract()

    def _get_factory_contract(self):
        factory_address = self.config.get_section('uniswap-factories')['v3']
        factory_contract = self.uniswap_client.get_factory_contract(factory_address)
        return factory_contract
    
    




if __name__ == '__main__':
    RuntimeTracker.start()
    pool_monitor = PoolMonitor()
    RuntimeTracker.stop()