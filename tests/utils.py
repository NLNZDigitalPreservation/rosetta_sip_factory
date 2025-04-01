import glob
import json
from os.path import join


def read_mets_files(base_path) -> list[str]:
    """
    Reads all mets files within a given directory and subdirectories.
    """
    data = []
    paths = glob.glob(join(base_path, "**", "mets.xml"), recursive=True)
    for path in paths:
        with open(path, "r", encoding="utf8") as file:
            data.append(file.read())
    return data


def read_json(path):
    with open(path, "r", encoding="utf8") as file:
        return json.load(file)
