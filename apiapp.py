from fastapi import FastAPI
from pymongo import MongoClient
from datetime import date, datetime


app = FastAPI()


@app.post("/readings", status_code=200)
async def fetch_readings(start_date: date = date.today(), end_date: date = date.today()):
    readings = []
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    with MongoClient("mongodb://root:pass@localhost:27017") as mongo_client:
        db = mongo_client["myapp"]
        collection = db["readings"]

        readings = list(collection.find(
            {"timestamp": {"$gte": start_date, "$lte": end_date}},
            {"_id": 0, "sensor_id": 1, "value": 1, "timestamp": 1}
        ))

        for reading in readings:
            parsed_timestamp = datetime.fromisoformat(reading["timestamp"])
            reading["timestamp"] = parsed_timestamp.strftime("%Y-%m-%d %H:%M:%S")

    return {"readings": readings}


@app.post("/sensor/latest/{sensor_id}", status_code=200)
async def fetch_readings(sensor_id: int):
    readings = []

    with MongoClient("mongodb://root:pass@localhost:27017") as mongo_client:
        db = mongo_client["myapp"]
        collection = db["readings"]

        readings = list(collection.find(
            {"sensor_id": sensor_id},
            {"_id": 0, "sensor_id": 1, "value": 1, "timestamp": 1}
        ).sort("_id", -1).limit(10))

        for reading in readings:
            parsed_timestamp = datetime.fromisoformat(reading["timestamp"])
            reading["timestamp"] = parsed_timestamp.strftime("%Y-%m-%d %H:%M:%S")

    return {"readings": readings}
