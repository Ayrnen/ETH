from classes.ethl_client import ETHLClient
from classes.runtime_tracker import RuntimeTracker

import asyncio

class Placeholder:
    def __init__(self):
        pass
    


if __name__ == '__main__':
    RuntimeTracker.start()
    web3_api = ETHLClient()

    loop = asyncio.get_event_loop()
    while True:
        # loop.run_until_complete(web3_api.get_pending_txn('0xC333E80eF2deC2805F239E3f1e810612D294F771'))
        loop.run_until_complete(web3_api.get_new_blocks())


    RuntimeTracker.stop()