import json

class ConfigUtils:

    @staticmethod
    def read_json_config(json_config_path):
        """

        :param json_config_path: Path of the json file
        :return:
        """
        config = {}
        try:
            with open(json_config_path, 'r') as file:
                config = json.load(file)

        except Exception as e:
            print(f"Error reading JSON configuration file: {e}")

        return config