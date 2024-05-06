# Using FastAPI to Build Python Web APIs

[This is the link of the tutorial](https://realpython.com/fastapi-python-web-apis/)

**Project Features**
- Automatic documentation.
    + Once the server is up, go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    + Alternative: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- Built-in serialization.

**Terms**
- Path: Refers to the last part of the URL starting from the first forward slash character.
    + Commonly called endpoint or route.
- Operation: The HTTP request method applied to the route.
    + FastAPI does not enforce a way to use these operations.
    + Types
        * POST
        * GET
        * PUT
        * DELETE
        * OPTIONS
        * HEAD
        * PATCH
        * TRACE

**Steps to execute**
- Manage dependencies using Poetry.
- Run it via `uvicorn_main:app_ --reload`
    - With `--reload` your application will reload automatically.

**Building your main handler.**
- Import fastapi.
- Create a FastAPI instance as `app`
- Map the route `/` and the operation `GET` to the function `root()`.
    + You can also add path parameters as `"/items/{item_id}"` that are processed as `root(item_id)`.
    + You can use type hints with these parameters via `root(item_id: int)`
        * This will return an error when something that cannot be deserialized to an integer is received.
- Define `root()` as an async function if you want concurrency and async/await.
- Return the content as a dictionary, list or singular values such as strings and integers.
    + They will be automatically converted to JSON, including ORMs and others.
- Data Handling with pedantic.
    - All the data validation is performed under the hood by pydantic.
- Order Matters: When creating path operations, put the **fixed paths before the parameterized ones**.


**Receiving JSON data**
- To send data from a client, you should use `POST`, `PUT`, `DELETE` or `PATCH`.
- You can use Pydantic to declare JSON Data Models or _Data Shapes_.
- Steps
    + Import `BaseModel` from pydantic.
    + Create a subclass defining the _schema_ or _data shapes_ you want to receive.
    + A JSON object that omits the default values is also valid.
    + 

*Example: FastAPI handling of a POST request with a body*
```python
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float # I do not agree with this, but this is an example.
    tax: Optional[float] = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item
```

With all this, FastAPI will:
1. Read the body of the request as JSON.
2. Convert the corresponding types if needed.
3. Validate the data and return a clear error if it is invalid.
4. Give you the received data in the parameter `item` as a type `Item` with editor support.
5. Generate JSON schema definitions for your model. 

