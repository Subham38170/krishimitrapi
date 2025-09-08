from fastapi import FastAPI
from fastapi.responses import JSONResponse


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