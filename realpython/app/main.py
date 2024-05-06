from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float # This is a terrible idea in production.
    tax: Optional[float] = None

class TaxedItem(Item):
    price_with_tax: float

app = FastAPI()

@app.get("/helloworld")
async def get_hello_world():
    return "Hello World"

@app.get("/items/integer/{item_id}")
async def read_item_parameter(item_id: int):
    return {"item_id": item_id}

@app.post("/items")
async def post_item(item: Item):
    return item

@app.put("/items/{item_id}")
async def put_item(item_id: int, item: Item):
    # Send back a json object instead of a concrete type.
    return {"item_id": item_id, **item.model_dump()}

@app.post("/items/tax")
async def apply_tax(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

