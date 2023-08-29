from fastapi import FastAPI
from pymongo import MongoClient
from datetime import date, datetime
import redis, json, os


app = FastAPI()


def connect_redis() -> redis:
    redis_ip = os.environ.get("REDIS_IP", "127.0.0.1")
    redis_port = os.environ.get("REDIS_PORT", "6379")

    return redis.Redis(host=redis_ip, port=redis_port, decode_responses=True)


@app.post("/readings", status_code=200)
async def fetch_readings(start_date: date = date.today(), end_date: date = date.today()):
    readings = []
    start_date = start_date.strftime("%Y-%m-%dT00:00:00")
    end_date = end_date.strftime("%Y-%m-%dT59:59:59")

    mongo_ip = os.environ.get("MONGO_IP", "127.0.0.1")
    mongo_port = os.environ.get("MONGO_PORT", "27017")
    mongo_username = os.environ.get("MONGO_USERNAME", "root")
    mongo_password = os.environ.get("MONGO_PASSWORD", "pass")
    mongo_database = os.environ.get("MONGO_DATABASE", "myapp")
    mongo_connect_uri = f"mongodb://{mongo_username}:{mongo_password}@{mongo_ip}:{mongo_port}"

    with MongoClient(mongo_connect_uri) as mongo_client:
        db = mongo_client[mongo_database]
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

    r = connect_redis()
    r_readings = r.lrange(f"sensor_id:{sensor_id}", 0, 9)

    for r_reading in r_readings:
        reading = json.loads(r_reading)
        parsed_timestamp = datetime.fromisoformat(reading["timestamp"])
        reading["timestamp"] = parsed_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        readings.append(reading)

    return {"readings": readings}
