import yaml
import os


def load_yaml_file(path: str):
    """
    Load yaml file from project directory.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    with open(path, "r") as f:
        return yaml.safe_load(f)
