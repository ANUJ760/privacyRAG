import re


def generate_collection_name(filename: str) -> str:
    """
    Convert a filename into a valid Chroma collection name.
    """

    name = filename.rsplit(".", 1)[0]

    name = name.lower()

    name = re.sub(r"[^a-z0-9]+", "_", name)

    return name.strip("_")