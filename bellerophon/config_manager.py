"""
config_manager.py

File containing the functionality to read config file and to provide
values of specified keys
"""
import json
import os


class ConfigManager:
    """
    ConfigManager class

    Class which handles the configuration realated functionalities.
    """
    current_dir = os.path.dirname(os.path.relpath(__file__))

    def __init__(self):
        self.filepath = os.path.join(self.current_dir, 'config.json')
        self.data = self.read_config()

    def read_config(self):
        """
        Function to read configuration from json file and store it in
        the class member `data`
        """
        try:
            with open(self.filepath, 'r') as json_file:
                data = json.load(json_file)
            return data
        except FileNotFoundError:
            raise FileNotFoundError('Configuration file missing')
        except json.decoder.JSONDecodeError:
            raise Exception('Configuration file is empty')

    def get_config(self, key):
        """
        Function to retrieve a sepecific configuration value by providing
        the correct key.

        :param string key: The key for the configuration which is to
        be retrieved

        :returns value object: The value for the key specified in arguments
        """
        try:
            return self.data[key]
        except KeyError:
            raise KeyError('The provided key is not there in config file')
