import os
import json

SUPPORTED_TYPES = (".pdfnc", ".pdfrm", ".pdcmd", ".pdobj")


def build_index(path):
    index = {}

    for file in os.listdir(path):
        name, ext = os.path.splitext(file)

        if ext.lower() in SUPPORTED_TYPES:
            index[name.upper()] = file

    index_path = os.path.join(path, "index.json")

    with open(index_path, "w") as f:
        json.dump(index, f, indent=4)

    return index