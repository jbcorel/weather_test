import requests
import json
from fastapi.exceptions import HTTPException

#TODO: after all done, check if country is needed at all
async def getCoordinates(cityName: str, country: str = None) -> dict:
    """Send a request to api-ninjas to get coordinates of a city."""
    key = 'jcnDTxl2p5vodbgalazywA==CPReURFTrfZ2yrrt'
    if country:
        api_url = 'https://api.api-ninjas.com/v1/city?name={}&country={}'.format(cityName, country)
    else:
        api_url = 'https://api.api-ninjas.com/v1/city?name={}'.format(cityName)
    try:
        rsp = requests.get(api_url, headers={'X-Api-Key': key}).json()
        rsp_dict = rsp[0]
    except Exception:
        return HTTPException(status_code=400, detail="Invalid city name")
    
    return rsp_dict

async def parseJsonForecast(json_forecast, name):
    """Parse json"""
    objFrst = json.loads(json_forecast.text)
    l_dates = objFrst['daily']['time']
    l_tmp_max = objFrst['daily']['temperature_2m_max']
    l_tmp_min = objFrst['daily']['temperature_2m_min']
    current_tmp = objFrst['current']['temperature_2m']
    tmp_join = list(zip(l_tmp_max, l_tmp_min))
    fcastDict = {'forecast': dict(zip(l_dates, tmp_join)),
                 'current': current_tmp,
                 'name': name, 
                 'status_code': 200}
    
    return fcastDict
    
async def getForecast(cityInfo: dict) -> dict:
    """Send coordinates to open-meteo API and get a json response"""
    city= cityInfo['name']
    country = cityInfo.get('country', None)
    coordinates = await getCoordinates(cityName=city, country=country)
    try:
        city = coordinates.get('name')
    except AttributeError:
        return coordinates
    latitude, longitude= coordinates['latitude'], coordinates['longitude']
    url = 'https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&daily=temperature_2m_max,temperature_2m_min&timezone=auto&current=temperature_2m'.format(latitude, longitude)
    try:
        forecast = requests.get(url)
    except ConnectionError: 
        return HTTPException(status_code=500, detail='Unable to establish connection with weather API. Try again later.')
    parsedForecast = await parseJsonForecast(forecast, city)
    return parsedForecast