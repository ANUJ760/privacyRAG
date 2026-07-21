import re


def generate_collection_name(filename: str) -> str:
    """
    Build a normalized Chroma collection name from an uploaded filename.

    The file extension is removed, the name is lowercased, and unsupported
    characters are collapsed into underscores.
    """

    name = filename.rsplit(".", 1)[0]

    name = name.lower()

    name = re.sub(r"[^a-z0-9]+", "_", name)

    return name.strip("_")
