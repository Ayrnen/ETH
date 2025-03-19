from classes.ethl_address_client import ETHLAddressClient
from classes.runtime_tracker import RuntimeTracker

import asyncio

class Placeholder:
    def __init__(self):
        pass
    


if __name__ == '__main__':
    RuntimeTracker.start()
    address_client = ETHLAddressClient('0xcAF6f896E07c95582a438CFe76f52a11D45c1CE7')

    print(address_client.get_balance_eth())
    print(address_client.get_transaction_count())
    print(address_client.get_balance_token('USDT'))
    

    RuntimeTracker.stop()