import re
import json
import datetime
from typing import NamedTuple
import os

import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

import time

INFLUXDB_ADDRESS = 'influxdb'
INFLUXDB_USER = 'mqtt'
INFLUXDB_PASSWORD = 'mqtt'
INFLUXDB_DATABASE = 'sensor_db'

MQTT_ADDRESS = 'mosquitto'
MQTT_USER = 'mqttuser'
MQTT_PASSWORD = 'mqttpassword'
MQTT_TOPIC = '#'
MQTT_REGEX = '([^/]+)/([^/]+)'
MQTT_CLIENT_ID = 'MQTTInfluxDBBridge'

DEBUG_DATA_FLOW = True
if os.getenv('DEBUG_DATA_FLOW') is not None:
    DEBUG_DATA_FLOW = os.getenv('DEBUG_DATA_FLOW')


influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)

def isfloat(x):
    try:
        a = float(x)
    except (TypeError, ValueError):
        return False
    else:
        return True

def isint(x):
    try:
        a = float(x)
        b = int(a)
    except (TypeError, ValueError):
        return False
    else:
        return a == b

def log(message):
    if DEBUG_DATA_FLOW:
        print(message)

class SensorData(NamedTuple):
    location: str
    measurement: str
    value: float
    timestamp: str
    station: str


def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    now = str(datetime.datetime.utcnow())
    now = now.split(".")[0]
    log_message = now + " Received a message by topic " + msg.topic
    print(log_message)

    payload = msg.payload.decode('utf-8')
    json_payload = json.loads(payload)
    timestamp_str = ""
    for key, value in json_payload.items():
        if "timestamp" in key:
            timestamp_str = value

    if timestamp_str:
        log_message = now + " Data timestamp is : " + timestamp_str
    else:
        log_message = now + " Data timestamp is : NOW"
    print(log_message)

    for key, value in json_payload.items():
        if isint(value) or isfloat(value):
            sensor_data = _parse_mqtt_message(msg.topic, key, float(value), timestamp_str)
            if sensor_data is not None:
                _send_sensor_data_to_influxdb(sensor_data)
                log_message = now + " " + sensor_data.location + "." + sensor_data.measurement + " " + str(sensor_data.value)
                print(log_message) 



def _parse_mqtt_message(topic, measurement, value, timestamp_str):
    match = re.match(MQTT_REGEX, topic)
    if match:
        location = match.group(1)
        station = match.group(2)
        measurm = station + "." + measurement
        return SensorData(location=location, measurement=measurm, value=value, timestamp=timestamp_str, station=station)
    else:
        return None


def _send_sensor_data_to_influxdb(sensor_data):
    date_time_str = sensor_data.timestamp
    timestamp = datetime.datetime.utcnow()
    if date_time_str:
        timestamp = datetime.datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%S%z")
    json_body = [
        {
            'measurement': sensor_data.measurement,
            'tags': {
                'location': sensor_data.location,
                'station' : sensor_data.station
            },
            'fields': {
                'value': sensor_data.value
            },
            'time' : timestamp
        }
    ]
    influxdb_client.write_points(json_body)


def _init_influxdb_database():
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        print('Creating database ' + INFLUXDB_DATABASE)
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)


def main():
    time.sleep(10)

    print('Connecting to the database ' + INFLUXDB_DATABASE)
    _init_influxdb_database()

    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()
