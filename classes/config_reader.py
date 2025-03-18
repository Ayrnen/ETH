import configparser
from web3 import Web3

class ConfigReader:
    def __init__(self):
        self.config_file = 'config.ini'
        self.config = configparser.ConfigParser()
        self._load_config()

    def _load_config(self):
        try:
            self.config.read(self.config_file)
        except Exception as e:
            raise ValueError(f'Error reading config file: {self.config_file}. {e}')

    def get_section(self, section):
        return {key: value for key, value in self.config[section].items()}

    def get_section_keys(self, section):
        return list(self.config[section].keys())
    
    def get_value(self, section, key):
        return self.config[section][key]

    def get_value_checksum(self, section, key):
        token_address = self.config[section][key]
        return Web3.to_checksum_address(token_address.lower())
