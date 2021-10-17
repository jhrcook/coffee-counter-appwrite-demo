from secrets import PROJECT_API_KEY
from typing import Any, Optional

from appwrite.client import Client
from appwrite.services.database import Database

from config import get_config

client = Client()

_config = get_config()

(
    client.set_endpoint(_config.appwrite.api_endpoint)
    .set_project(_config.appwrite.project_id)
    .set_key(PROJECT_API_KEY)
)


def _get_coffee_bag_db() -> Database:
    db = Database(client)
    return db


def _get_coffee_bag_collections_id() -> str:
    return _config.appwrite.collections.coffee_bag_collection_id


def get_coffee_bags(
    brand: Optional[str], active: Optional[bool] = None
) -> dict[str, Any]:
    db = _get_coffee_bag_db()

    filters = []
    if brand is not None:
        filters.append(f"brand={brand}")
    if active is not None:
        filters.append(f"active={int(active)}")

    print(filters)
    coffee_bags_dict = db.list_documents(
        _get_coffee_bag_collections_id(), filters=filters
    )
    return coffee_bags_dict


def get_coffee_bag(id: str) -> dict[str, Any]:
    db = _get_coffee_bag_db()
    return db.get_document(
        collection_id=_get_coffee_bag_collections_id(), document_id=id
    )
