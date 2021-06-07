from typing import List, Text
import requests

import databases
import sqlalchemy
from fastapi import FastAPI, Response, status
from sqlalchemy import sql
from sqlalchemy.sql.schema import ForeignKey
from starlette.responses import Response

DATABASE_URL = "postgresql://linx:linx123@127.0.0.1:5432/weather"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

city_info = sqlalchemy.Table(
    "city_info",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("cod", sqlalchemy.String),
    sqlalchemy.Column("message", sqlalchemy.Integer),
    sqlalchemy.Column("cnt", sqlalchemy.Integer),
    sqlalchemy.Column("city_id", sqlalchemy.Integer),
    sqlalchemy.Column("city_name", sqlalchemy.String),
    sqlalchemy.Column("coord_lat", sqlalchemy.DECIMAL),
    sqlalchemy.Column("coord_lon", sqlalchemy.DECIMAL),
    sqlalchemy.Column("country", sqlalchemy.String),
    sqlalchemy.Column("population", sqlalchemy.Integer),
    sqlalchemy.Column("timezone", sqlalchemy.Integer),
    sqlalchemy.Column("sunrise", sqlalchemy.Integer),
    sqlalchemy.Column("sunset", sqlalchemy.Integer),
)

city_weather = sqlalchemy.Table(
    "city_weather",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer,ForeignKey("city_info.id")),
    sqlalchemy.Column("dt", sqlalchemy.Integer),
    sqlalchemy.Column("main_feels_like", sqlalchemy.DECIMAL),
    sqlalchemy.Column("main_temp_min", sqlalchemy.DECIMAL),
    sqlalchemy.Column("main_temp_max", sqlalchemy.DECIMAL),
    sqlalchemy.Column("main_pressure", sqlalchemy.Integer),
    sqlalchemy.Column("main_sea_level", sqlalchemy.Integer),
    sqlalchemy.Column("main_grnd_level", sqlalchemy.Integer),
    sqlalchemy.Column("main_humidity", sqlalchemy.Integer),
    sqlalchemy.Column("main_temp_kf", sqlalchemy.DECIMAL),
    sqlalchemy.Column("weather_id", sqlalchemy.Integer),
    sqlalchemy.Column("weather_main", sqlalchemy.String),
    sqlalchemy.Column("weather_description", sqlalchemy.String),
    sqlalchemy.Column("weather_icon", sqlalchemy.String),
    sqlalchemy.Column("clouds_all", sqlalchemy.Integer),
    sqlalchemy.Column("wind_speed", sqlalchemy.DECIMAL),
    sqlalchemy.Column("wind_deg", sqlalchemy.Integer),
    sqlalchemy.Column("wind_gust", sqlalchemy.DECIMAL),
    sqlalchemy.Column("visibility", sqlalchemy.Integer),
    sqlalchemy.Column("pop", sqlalchemy.Integer),
    sqlalchemy.Column("sys_pod", sqlalchemy.String),
    sqlalchemy.Column("dt_txt", sqlalchemy.String)
)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/history/{city}",status_code=200)
async def read_historic(city, response: Response):
    """
        Retorna o historico de busca salvo no banco de dados.
    """

    query = sql.text(
                "with city as (select * from city_info where upper(city_name) = upper(:c))"
                "select * from city as c INNER join city_weather as cw ON c.id = cw.id"
            ).params(c=city)
    result = await database.fetch_all(query)
    if result == []:
        response.status_code= status.HTTP_404_NOT_FOUND
        return {"Message":"City not found"}
    
    return result 



@app.post("/search/{city}",status_code=200)
async def read_root(city: str, response: Response):
    """
        Busca e grava dados do clima de acordo com a cidade informada
    """
    result = requests.get('http://api.openweathermap.org/data/2.5/forecast?',params={'q':city,'appid':'dbc212b36586871ca53b41cc19a35a3a'})
    data = result.json()
    if data["cod"] != "200":
        response.status_code= status.HTTP_404_NOT_FOUND
        return data

    query = city_info.insert().values(
        cod=data["cod"], 
        message=data["message"],
        cnt=data["cnt"],
        city_id=data["city"]["id"],
        city_name=data["city"]["name"],
        coord_lat=data["city"]["coord"]["lat"],
        coord_lon=data["city"]["coord"]["lon"],
        country=data["city"]["country"],
        population=data["city"]["population"],
        timezone=data["city"]["timezone"],
        sunrise=data["city"]["sunrise"],
        sunset=data["city"]["sunset"]
    )
    last_record_id = await database.execute(query)

    for item in data["list"]:
        query_city_weather = city_weather.insert().values(
                id=last_record_id,
                dt=item["dt"],
                main_feels_like=item["main"]["feels_like"],
                main_temp_min=item["main"]["temp_min"],
                main_temp_max=item["main"]["temp_max"],
                main_pressure=item["main"]["pressure"],
                main_sea_level=item["main"]["sea_level"],
                main_grnd_level=item["main"]["grnd_level"],
                main_humidity=item["main"]["humidity"],
                main_temp_kf=item["main"]["temp_kf"],
                weather_id=item["weather"][0]["id"],
                weather_main=item["weather"][0]["main"],
                weather_description=item["weather"][0]["description"],
                weather_icon=item["weather"][0]["icon"],
                clouds_all=item["clouds"]["all"],
                wind_speed=item["wind"]["speed"],
                wind_deg=item["wind"]["deg"],
                wind_gust=item["wind"]["gust"],
                visibility=item["visibility"],
                pop=item["pop"],
                sys_pod=item["sys"]["pod"],
                dt_txt=item["dt_txt"]
        )
        await database.execute(query_city_weather)

    return {"Message": "Information saved"}