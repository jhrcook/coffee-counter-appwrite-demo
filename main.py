from datetime import date, datetime
from typing import Optional

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
    roast: Optional[CoffeeBeanRoast] = None,
    active: Optional[bool] = None,
) -> list[CoffeeBagDocument]:
    coffee_bags = ab.get_coffee_bags(brand=brand, active=active, roast=roast)

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
    return ab.get_coffee_bag(bag_id)


@app.get("/cups")
def coffee_cups(
    start: Optional[datetime] = None, coffee_bag_id: Optional[BagID] = None
) -> list[CoffeeCupDocument]:
    cups = ab.get_coffee_cups(bag_id=coffee_bag_id)

    if start is not None:
        cups = list(filter(lambda c: start <= c.datetime, cups))

    return cups


@app.get("/cups/{cup_id}")
def coffee_cup(cup_id: str) -> CoffeeCupDocument:
    return ab.get_coffee_cup(id=cup_id)


@app.put("/bag")
def new_coffee_bag(coffee_bag: CoffeeBag) -> CoffeeBagDocument:
    return ab.add_coffee_bag(coffee_bag)


@app.put("/cup")
def new_cup(coffee_cup: CoffeeCup) -> CoffeeCupDocument:
    return ab.add_coffee_cup(coffee_cup=coffee_cup)
