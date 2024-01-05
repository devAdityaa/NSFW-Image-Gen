from gen import main
from fastapi import FastAPI, Header, Body
from typing import Annotated


app = FastAPI()
def urlencode_dict(data):
    """
    Convert a dictionary to x-www-form-urlencoded format.
    """
    encoded_data = "&".join([f"{key}={value}" for key, value in data.items()])
    return encoded_data
#Handling Errors
def error_handler(e:Exception):
    return {"error":str(e)}

@app.post('/create')
async def gen(messages : dict[str, str] = Body(...)):
    data = urlencode_dict(messages)
    url = await main(data)
    return url