import random
from paho.mqtt import client as mqtt_client
from pymongo import MongoClient
import json


broker = '127.0.0.1'
port = 1883
topic = "python/mqtt"
client_id = f'subscribe-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        message = msg.payload.decode()
        message_obj = json.loads(message)

        with MongoClient("mongodb://root:pass@localhost:27017") as mongo_client:
            db = mongo_client["myapp"]
            readings_collection = db["readings"]
            result = readings_collection.insert_one(message_obj)
            print(message)

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
