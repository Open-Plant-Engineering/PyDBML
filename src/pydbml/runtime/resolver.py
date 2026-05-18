import os


class ResourceResolver:

    def __init__(self, config):
        self.config = config

    def resolve(self, name):
        name = name.upper()

        for base_path in self.config.paths:
            index_file = os.path.join(base_path, "index.txt")

            if not os.path.exists(index_file):
                continue

            with open(index_file) as f:
                for line in f:
                    line = line.strip()

                    if not line:
                        continue

                    # ✅ Extract file name
                    rel_path = line

                    file_name = os.path.basename(rel_path)
                    base_name, ext = os.path.splitext(file_name)

                    if base_name.upper() == name:
                        full_path = os.path.join(base_path, rel_path)

                        if os.path.exists(full_path):
                            return full_path

        import os


class ResourceResolver:

    def __init__(self, config):
        self.config = config

    def resolve(self, name):
        name = name.upper()

        for base_path in self.config.paths:
            index_file = os.path.join(base_path, "index.txt")

            if not os.path.exists(index_file):
                continue

            with open(index_file) as f:
                for line in f:
                    line = line.strip()

                    if not line:
                        continue

                    # ✅ Extract file name
                    rel_path = line

                    file_name = os.path.basename(rel_path)
                    base_name, ext = os.path.splitext(file_name)

                    if base_name.upper() == name:
                        full_path = os.path.join(base_path, rel_path)

                        if os.path.exists(full_path):
                            return full_path

        raise FileNotFoundError(
            f"{name} not found in PYDBML_LIB paths: {self.config.paths}"
        )