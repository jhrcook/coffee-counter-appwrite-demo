import re
from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, PositiveFloat


class AppwriteDocumentPermissions(BaseModel):
    """Appwrite document permissions."""

    read: list[str]
    write: list[str]


class AppwriteDocument(BaseModel):
    """Basic fields for an Appwrite document."""

    id: str
    collection: str
    permissions: AppwriteDocumentPermissions

    def __init__(self, **kwargs) -> None:
        for k in list(kwargs.keys()):
            if isinstance(k, str):
                _k = re.sub("^\\$", "", k)
                kwargs[_k] = kwargs.pop(k)
        super().__init__(**kwargs)


class CoffeeBeanRoast(Enum):
    """Types of roasts."""

    LIGHT = "LIGHT"
    LIGHT_MEDIUM = "LIGHT_MEDIUM"
    MEDIUM = "MEDIUM"
    MEDIUM_DARK = "MEDIUM_DARK"
    DARK = "DARK"
    FRENCH = "FRENCH"
    ESPRESSO = "ESPRESSO"


class CoffeeBag(BaseModel):
    """Coffee bag data."""

    brand: str
    name: str
    mass: PositiveFloat
    start_date: date
    end_date: date
    active: bool
    roast: CoffeeBeanRoast


class CoffeeBagDocument(CoffeeBag, AppwriteDocument):
    """Coffee Bag Document."""


class CoffeeCup(BaseModel):
    """Coffee cup data."""

    bag_id: str
    datetime: datetime


class CoffeeCupDocument(CoffeeCup, AppwriteDocument):
    """Coffee Cup Document."""
