from datetime import date, datetime
from pprint import pprint
from typing import Callable, Optional

from fastapi import FastAPI

import appwrite_backend as ab
from models import (
    CoffeeBag,
    CoffeeBagDocument,
    CoffeeBeanRoast,
    CoffeeCup,
    CoffeeCupDocument,
)

app = FastAPI()

BagID = str
CupID = str


@app.get("/")
def root():
    return {"message": "Coffee Counter v2"}


@app.get("/bags")
def coffee_bags(
    start: Optional[date] = None,
    end: Optional[date] = None,
    brand: Optional[str] = None,
    active: Optional[bool] = None,
) -> list[CoffeeBagDocument]:
    coffee_bags_dict = ab.get_coffee_bags(brand=brand, active=active)
    pprint(coffee_bags_dict)
    coffee_bags = [CoffeeBagDocument(**info) for info in coffee_bags_dict["documents"]]

    if start is not None:
        coffee_bags = list(
            filter(
                lambda b: (b.start_date is None) or (start <= b.start_date), coffee_bags
            )
        )
    if end is not None:
        coffee_bags = list(
            filter(lambda b: (b.end_date is None) or (b.end_date <= end), coffee_bags)
        )

    return coffee_bags


@app.get("/bags/{bag_id}")
def coffee_bag(bag_id: str) -> CoffeeBagDocument:
    return CoffeeBagDocument(**ab.get_coffee_bag(bag_id))


@app.get("/cups")
def coffee_cups(
    start: Optional[datetime] = None, coffee_bag_id: Optional[BagID] = None
):
    pass


@app.get("/cups/{cup_id}")
def coffee_cup(cup_id: str) -> CoffeeCupDocument:
    pass


@app.put("/bag")
def new_coffee_bag(coffee_bag: CoffeeBag) -> CoffeeBagDocument:
    res = ab.add_coffee_bag(coffee_bag)
    return CoffeeBagDocument(**res)


@app.put("/cup")
def new_cup(coffee_cup: CoffeeCup) -> CoffeeCupDocument:
    pass
