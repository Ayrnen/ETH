from classes.web3_client2 import Web3Client
from classes.runtime_tracker import RuntimeTracker
from classes.config_reader import ConfigReader

import asyncio

class Placeholder:
    def __init__(self):
        pass
    


if __name__ == '__main__':
    RuntimeTracker.start()
    web3_api = Web3Client()

    if __name__ == "__main__":
        loop = asyncio.get_event_loop()
        while True:
            loop.run_until_complete(web3_api.get_new_blocks())


    RuntimeTracker.stop()