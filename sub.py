# python3.6

import random
import base64, binascii
import re

from paho.mqtt import client as mqtt_client


broker = 'apidev.sucofindo.co.id'
port = 1883
topic = "CAM001/send"
# Generate a Client ID with the subscribe prefix.
client_id = f'SVR-sub-{random.randint(0, 100)}'
username = 'tally'
password = 'tally'

def is_base64(base64_string):
    base64_string = base64_string[base64_string.find(",")+1:]
    expression = "^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$"

    matches = re.match(expression, base64_string)
    msg = "not base64 string"
    if matches:
        msg = "base64 string"
    return msg

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    # client.connect_async(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if is_base64(msg.payload.decode()):
            base64_string = msg.payload.decode()
            base64_string = base64_string[base64_string.find(",")+1:]
            try:
                image = base64.b64decode(base64_string, validate=True)
                file_to_save = "CAM001_image.png"
                with open(file_to_save, "wb") as f:
                    f.write(image)
            except binascii.Error as e:
                print(e)

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
