# abi_loader.py
import json
import os
from pathlib import Path

class ABIReader:
    def __init__(self, service):
        self.base_dir = Path('abis/' + service)
        self._abi_cache = {}  # Cache loaded ABIs for speed

    def get_abi(self, contract_name):
        if contract_name in self._abi_cache:
            return self._abi_cache[contract_name]

        abi_path = self.base_dir / f'{contract_name}.json'
        if not abi_path.exists():
            raise FileNotFoundError(f'No ABI found for {contract_name} at {abi_path}')

        with open(abi_path, 'r') as f:
            abi = json.load(f)
            self._abi_cache[contract_name] = abi
            return abi

    def get_abi_by_address(self, address):
        address_to_abi = {
            '0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640': 'weth_usdc_v3_05',
            '0x4e68Ccd3E89f51C3074ca5072bbAC773960dFa36': 'weth_usdt_v3_3',
        }
        contract_name = address_to_abi.get(address)
        if not contract_name:
            raise ValueError(f'No ABI mapped to address {address}')
        return self.get_abi(contract_name)