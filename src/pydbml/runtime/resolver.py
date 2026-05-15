import os
import json


class ResourceResolver:

    def __init__(self, config):
        self.config = config

    def resolve(self, name, extension):
        name = name.upper()

        for path in self.config.paths:
            index_file = os.path.join(path, "index.json")

            if not os.path.exists(index_file):
                continue

            with open(index_file) as f:
                index = json.load(f)

            if name in index:
                file_path = os.path.join(path, index[name])

                if file_path.endswith(extension):
                    return file_path

        raise FileNotFoundError(f"{name}{extension} not found")