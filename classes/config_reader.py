import configparser

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
        if section not in self.config:
            raise KeyError(f"Section '{section}' not found in config file: {self.config_file}")
        return {key: value for key, value in self.config[section].items()}
