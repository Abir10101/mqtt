import random
from paho.mqtt import client as mqtt_client
from datetime import datetime
import json


broker = '127.0.0.1'
port = 1883
topic = "python/mqtt"
client_id = f'publish-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

def connect_mqtt():
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


def publish(client):
    sensor_id = 1111
    reading_value = "demo limited value"
    timestamp = datetime.now().isoformat()

    message = {
        "sensor_id": sensor_id,
        "value": reading_value,
        "timestamp": timestamp
    }

    result = client.publish(topic, json.dumps(message))

    status = result[0]
    if status == 0:
        print(f"Send `{message}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()
