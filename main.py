from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from typing import Annotated,Literal,Optional
from deep_translator import GoogleTranslator


import json
import requests


api_key = '579b464db66ec23bdd000001d3ad78691ec4401741103c451d555ca6'

indian_languages ={
 'Hindi': 'hi', 'Bengali': 'bn', 'Telugu': 'te', 'Tamil': 'ta', 'Kannada': 'kn',
 'Malayalam': 'ml', 'Marathi': 'mr', 'Punjabi': 'pa', 'Gujarati': 'gu', 'Odia': 'or',
 'Assamese': 'as', 'Sindhi': 'sd', 'Nepali': 'ne', 'Sinhala': 'si', 'Urdu': 'ur',
 'Kashmiri': 'ks', 'Bihari': 'bh', 'Bodo': 'brx', 'Maithili': 'mai', 'Manipuri': 'mni',
 'Sanskrit': 'sa'
}




class MandiApiRequest(BaseModel):
    api_key: Annotated[str, Field(default=api_key, description="Your API Key",alias='api-key')]
    format: Annotated[Literal['json','xml','csv'], Field(default='json', description="Default is json", examples=['json','xml','csv'])]
    offset: Optional[int] = Field(default=None, description='number of records to skip for pagination')
    limit: Optional[int] = Field(default=None, description='maximum number of records to return')
    filters_state: Optional[str] = Field(default=None, alias="filters[state.keyword]")
    filters_district: Optional[str] = Field(default=None, alias="filters[district]")
    filters_market: Optional[str] = Field(default=None, alias="filters[market]")
    filters_commodity: Optional[str] = Field(default=None, alias="filters[commodity]")
    filters_variety: Optional[str] = Field(default=None, alias="filters[variety]")
    filters_grade: Optional[str] = Field(default=None, alias="filters[grade]")


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


@app.post('/mandiprices')
def get_mandi(request: MandiApiRequest,lang: str):
    url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

    
    # Build query params
    params = request.model_dump(by_alias=True,exclude_none=True)

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

     
        data = response.json()
        if lang != 'en':
            try:
                trans = GoogleTranslator('en',indian_languages[lang])
                convert = trans.translate(str(data))
                data = convert
            except Exception as e:
                return JSONResponse(status_code=500, content={"error": str(e)})




        return {'data': data}

    except requests.RequestException as e:
        return JSONResponse(status_code=500, content={"error": str(e)})