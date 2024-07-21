from fastapi import FastAPI, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from . import external

app = FastAPI()
app.mount("/static", StaticFiles(directory="client/static"), name='static')

templates = Jinja2Templates(directory="client/templates")

@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="base.html"
    )

@app.get('/get-weather')
async def getWeather(city: str = ..., country: Annotated[str | None, Query(max_length=2)] = None):
    """Main endpoint for getting forecasts"""
    queryDict = {"name": city, "country": country}    
    forecast = await external.getForecast(queryDict)
    return forecast

