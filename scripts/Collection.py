import os


def collect_py_files(root_dir, output_txt, skip_dirs=None):
    if skip_dirs is None:
        skip_dirs = set()

    skip_dirs = {d.lower() for d in skip_dirs}

    with open(output_txt, "w", encoding="utf-8") as out_file:
        for foldername, subfolders, filenames in os.walk(root_dir):
            # Remove skipped directories (prevents os.walk from entering them)
            subfolders[:] = [sf for sf in subfolders if sf.lower() not in skip_dirs]

            for filename in filenames:
                if filename.endswith(".py"):
                    file_path = os.path.join(foldername, filename)

                    # Avoid including the output file itself
                    if os.path.abspath(file_path) == os.path.abspath(output_txt):
                        continue

                    out_file.write(f"# FILE: {file_path}\n")
                    out_file.write("-" * 80 + "\n")

                    try:
                        with open(
                            file_path, "r", encoding="utf-8", errors="replace"
                        ) as py_file:
                            out_file.write(py_file.read())
                    except Exception as e:
                        out_file.write(f"[Error reading file: {e}]")

                    out_file.write("\n\n")  # space between files


if __name__ == "__main__":
    directory_to_scan = r"C:\SKRepo\OpePyDBML\src"
    output_file = "all_python_code.txt"

    skip_folders = {
        "vendor\OPE_DB_API",
        "vendor\PyDBML",
    }

    collect_py_files(directory_to_scan, output_file, skip_folders)

    skip_folders = {}
    collect_py_files(
        r"C:\SKRepo\OPETreeWB\vendor\OPE_DB_API\OPE_DB_API",
        "OPE_DB_API.txt",
        skip_folders,
    )
    collect_py_files(
        r"C:\SKRepo\OPETreeWB\vendor\PyDBML\PyDBML", "PyDBML.txt", skip_folders
    )
    print("Done! Python files have been consolidated.")
