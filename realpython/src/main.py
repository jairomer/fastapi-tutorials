#from typing import Optional

from fastapi import FastAPI
#from pydantic import BaseModel

app = FastAPI()

@app.get("/helloworld")
async def get_hello_world():
    return "Hello World"

