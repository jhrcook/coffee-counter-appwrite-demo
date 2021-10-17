from secrets import PROJECT_API_KEY
from typing import Optional

from appwrite.client import Client
from appwrite.services.database import Database

from config import get_config
from models import (
    CoffeeBag,
    CoffeeBagDocument,
    CoffeeBeanRoast,
    CoffeeCup,
    CoffeeCupDocument,
)

client = Client()

_config = get_config()

(
    client.set_endpoint(_config.appwrite.api_endpoint)
    .set_project(_config.appwrite.project_id)
    .set_key(PROJECT_API_KEY)
)


def _get_database() -> Database:
    db = Database(client)
    return db


def _get_coffee_bag_collections_id() -> str:
    return _config.appwrite.collections.coffee_bag_collection_id


def _get_coffee_cup_collections_id() -> str:
    return _config.appwrite.collections.coffee_cup_collection_id


# ---- Coffee Bags ----


def get_coffee_bags(
    brand: Optional[str], active: Optional[bool], roast: Optional[CoffeeBeanRoast]
) -> list[CoffeeBagDocument]:
    db = _get_database()

    filters = []
    if brand is not None:
        filters.append(f"brand={brand}")
    if active is not None:
        filters.append(f"active={int(active)}")
    if roast is not None:
        filters.append(f"roast={roast}")

    print(filters)
    res = db.list_documents(_get_coffee_bag_collections_id(), filters=filters)
    return [CoffeeBagDocument(**info) for info in res["documents"]]


def get_coffee_bag(id: str) -> CoffeeBagDocument:
    db = _get_database()
    res = db.get_document(
        collection_id=_get_coffee_bag_collections_id(), document_id=id
    )
    return CoffeeBagDocument(**res)


def add_coffee_bag(coffee_bag: CoffeeBag) -> CoffeeBagDocument:
    db = _get_database()
    res = db.create_document(
        collection_id=_get_coffee_bag_collections_id(), data=coffee_bag.json()
    )
    return CoffeeBagDocument(**res)


# ---- Coffee Cups ----


def get_coffee_cups(bag_id: Optional[str]) -> list[CoffeeCupDocument]:
    db = _get_database()

    filters = []
    if bag_id is not None:
        filters.append(f"bag_id={bag_id}")

    res = db.list_documents(_get_coffee_cup_collections_id(), filters=filters)
    return [CoffeeCupDocument(**info) for info in res["documents"]]


def get_coffee_cup(id: str) -> CoffeeCupDocument:
    db = _get_database()
    res = db.get_document(
        collection_id=_get_coffee_cup_collections_id(), document_id=id
    )
    return CoffeeCupDocument(**res)


def add_coffee_cup(coffee_cup: CoffeeCup) -> CoffeeCupDocument:
    db = _get_database()
    res = db.create_document(
        collection_id=_get_coffee_cup_collections_id(), data=coffee_cup.json()
    )
    return CoffeeCupDocument(**res)
