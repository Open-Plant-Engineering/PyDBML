import shutil
from pathlib import Path


def remove_pycache(root_dir):
    for pycache in Path(root_dir).rglob("__pycache__"):
        if pycache.is_dir():
            shutil.rmtree(pycache)


# Example usage
remove_pycache(r"C:\SKRepo\OpePyDBML")  # current directory
