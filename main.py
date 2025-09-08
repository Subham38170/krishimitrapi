from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from typing import Annotated


class Message(BaseModel):
    msg: Annotated[str,Field(...,description="Enter the message")]



app = FastAPI()


@app.get('/')
def about():
    return JSONResponse(
        status_code=200,
        content={'Message':'Welcome to this krishi Mitra App'}
    )


@app.get('/about')
def get_about():
    return {'About ': 'This is the api for krishimitra'}


@app.post('/sentence')
def translate(sen: Message):
    return {'Your data is ': sen.msg}
