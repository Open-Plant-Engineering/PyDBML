class RuntimeConfig:
    def __init__(self, paths=None):
        self.paths = paths or []

    def add_path(self, path):
        self.paths.append(path)
