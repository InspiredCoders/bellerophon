import json
import os


class ConfigManager:

    current_dir = os.path.dirname(os.path.relpath(__file__))

    def __init__(self):
        self.filepath = os.path.join(self.current_dir, 'config.json')
        self.data = self.read_config()

    def read_config(self):
        try:
            with open(self.filepath, 'r') as json_file:
                data = json.load(json_file)
            return data
        except FileNotFoundError:
            raise FileNotFoundError('Configuration file missing')
        except json.decoder.JSONDecodeError:
            raise Exception('Configuration file is empty')

    def get_config(self, key):
        try:
            return self.data[key]
        except KeyError:
            raise KeyError('The provided key is not there in config file')


if __name__ == '__main__':
    config = ConfigManager()
