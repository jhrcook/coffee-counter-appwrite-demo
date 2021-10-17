from pathlib import Path
from typing import Final

import yaml
from pydantic import BaseModel

_config_path: Final[Path] = Path("config.yml")


class AppwriteCollectionsConfig(BaseModel):

    coffee_bag_collection_id: str


class AppwriteConfig(BaseModel):

    project_id: str
    api_endpoint: str
    collections: AppwriteCollectionsConfig


class ProjectConfig(BaseModel):

    appwrite: AppwriteConfig


def get_config() -> ProjectConfig:
    with open(_config_path, "r") as config_file:
        config_data = yaml.safe_load(config_file)
    return ProjectConfig(**config_data)
