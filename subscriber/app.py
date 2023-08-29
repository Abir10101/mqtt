import os, json, redis, random
from paho.mqtt import client as mqtt_client
from pymongo import MongoClient


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    broker_ip = os.environ.get("MESSAGE_BROKER_IP", "127.0.0.1")
    broker_port = os.environ.get("MESSAGE_BROKER_PORT", "1883")
    broker_port = int(broker_port)
    broker_client_id = f'subscribe-{random.randint(0, 100)}'
    # username = 'emqx'
    # password = 'public'

    client = mqtt_client.Client(broker_client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker_ip, broker_port)
    return client


def connect_redis() -> redis:
    redis_ip = os.environ.get("REDIS_IP", "127.0.0.1")
    redis_port = os.environ.get("REDIS_PORT", "6379")

    return redis.Redis(host=redis_ip, port=redis_port, decode_responses=True)


def cache_readings(r :redis, key :int, message :str):
    r.lpush(key, message)
    r.ltrim(key, 0, 9)


def subscribe(client: mqtt_client):
    mongo_ip = os.environ.get("MONGO_IP", "127.0.0.1")
    mongo_port = os.environ.get("MONGO_PORT", "27017")
    mongo_username = os.environ.get("MONGO_USERNAME", "root")
    mongo_password = os.environ.get("MONGO_PASSWORD", "pass")
    mongo_database = os.environ.get("MONGO_DATABASE", "myapp")
    mongo_connect_uri = f"mongodb://{mongo_username}:{mongo_password}@{mongo_ip}:{mongo_port}"

    def on_message(client, userdata, msg):
        message = msg.payload.decode()
        message_obj = json.loads(message)
        print(message)

        with MongoClient(mongo_connect_uri) as mongo_client:
            db = mongo_client[mongo_database]
            readings_collection = db["readings"]
            result = readings_collection.insert_one(message_obj)

        r = connect_redis()
        sensor_id = message_obj["sensor_id"]
        r_key = f"sensor_id:{sensor_id}"
        cache_readings(r, r_key, message)

    broker_topic = "python/mqtt"

    client.subscribe(broker_topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
