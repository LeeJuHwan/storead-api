import environ
import os
import yaml

from pathlib import Path

ENV = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
ROOT_DIR = Path(__file__).resolve().parent.parent
APP_DIR = ROOT_DIR / "core_apps"
super_secret_yaml = Path(ROOT_DIR, "config", "settings", ".social.yaml")


def load_yaml_file(path: Path):
    """
    Load yaml file from project directory.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    with open(path, "r") as f:
        return yaml.safe_load(f)
