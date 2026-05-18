import os

class RuntimeConfig:
    def __init__(self, paths=None):
        self.paths = paths or []

        env_paths = os.getenv("PYDBML_LIB", "")
        for p in env_paths.split(os.pathsep):
            if p:
                self.add_path(p)

    def add_path(self, path):
        if path not in self.paths:
            self.paths.append(path)

