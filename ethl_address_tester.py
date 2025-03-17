from classes.ethl_address_client import ETHLAddressClient
from classes.runtime_tracker import RuntimeTracker

import asyncio

class Placeholder:
    def __init__(self):
        pass
    


if __name__ == '__main__':
    RuntimeTracker.start()
    address_client = ETHLAddressClient('0xC333E80eF2deC2805F239E3f1e810612D294F771')

    print(address_client.get_balance())
    print(address_client.get_transactions())
    

    RuntimeTracker.stop()