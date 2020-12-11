import argparse
import sys
from urllib.parse import urljoin

import paho.mqtt.client as mqtt

HOST = "broker.hivemq.com"
topic = "sprc/chat/#"


def on_connect(client, userdata, flags, rc):

    print("Connected with result code " + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode('utf-8')))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(HOST, 1883, 60)
client.loop_start()

while True:
    msg = input()
    client.publish("sprc/chat/AlexandraMinea", msg)

client.disconnect()
client.loop_stop()