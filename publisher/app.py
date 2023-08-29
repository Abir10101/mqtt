import random, os
from paho.mqtt import client as mqtt_client
from datetime import datetime
import json


def connect_mqtt():
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


def publish(client):
    sensor_id = random.randint(0, 3)
    reading_value = "demo value"
    timestamp = datetime.now().isoformat()

    message = {
        "sensor_id": sensor_id,
        "value": reading_value,
        "timestamp": timestamp
    }

    broker_topic = "python/mqtt"

    result = client.publish(broker_topic, json.dumps(message))

    status = result[0]
    if status == 0:
        print(f"Send `{message}` to topic `{broker_topic}`")
    else:
        print(f"Failed to send message to topic {broker_topic}")


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()
