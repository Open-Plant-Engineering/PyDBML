import os


SUPPORTED = (".pdfnc", ".pdfrm", ".pdcmd", ".pdobj")


def build_index(path):
    entries = []

    for root, dirs, files in os.walk(path):
        for file in files:
            ext = os.path.splitext(file)[1].lower()

            if ext not in SUPPORTED:
                continue

            rel_dir = os.path.relpath(root, path)

            if rel_dir == ".":
                rel_path = file
            else:
                rel_path = f"{rel_dir}/{file}"

            entries.append(rel_path)

    index_file = os.path.join(path, "index.txt")

    with open(index_file, "w") as f:
        f.write("\n".join(entries))