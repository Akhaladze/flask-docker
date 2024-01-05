import time
import paho.mqtt.client as mqtt
import os
from celery import shared_task, Task
import requests
MQTT_BROKER_URL = os.environ.get("MQTT_BROKER_URL", '192.168.88.229')
MQTT_BROKER_PORT = int(os.environ.get("MQTT_BROKER_PORT", 1883))
MQTT_BROKER_TIMEOUT = int(os.environ.get("MQTT_BROKER_TIMEOUT", 60))

CRATEDB_URL = os.environ.get("CRATEDB_API_URL", 'http://192.168.88.238:5040')
CRATEDB_USER = os.environ.get("CRATEDB_USER", 'crate')
CRATEDB_PASSWORD = os.environ.get("CRATEDB_PASSWORD", '')


@shared_task(ignore_result=False)
def add(a: int, b: int) -> int:
    return a + b


@shared_task()
def block() -> None:
    time.sleep(5)


@shared_task(bind=True, ignore_result=False)
def process(self: Task, total: int) -> object:
    for i in range(total):
        self.update_state(state="PROGRESS", meta={"current": i + 1, "total": total})
        time.sleep(1)

    return {"current": total, "total": total}


@shared_task(ignore_result=False)
def getShellyStatuses():
    def on_connect(client, userdata, flags, rc):
        print("Connected to MQTT broker")
        #client.subscribe("#")  # Subscribe to all topics
        client.subscribe("shellypro4pm-c8f09e87c674/status/#")

    def on_message(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        requests.post(CRATEDB_URL + '/_sql?types', auth=(CRATEDB_USER, CRATEDB_PASSWORD), data='INSERT INTO device_statuses (device_id, status, data, created_at, updated_at) VALUES (?, ?, ?, ?, ?)', params=(msg.topic, 'online', msg.payload, 'now', 'now'))
        

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT, MQTT_BROKER_TIMEOUT)
    client.loop_forever()

@shared_task(ignore_result=False)
def getShellyEvents():
	def on_connect(client, userdata, flags, rc):
		print("Connected to MQTT broker (events)")
		client.subscribe("shellypro4pm-c8f09e87c674/events/#")
        

	def on_message(client, userdata, msg):
		print(msg.topic + " " + str(msg.payload))
		requests.post(CRATEDB_URL + '/_sql?types', auth=(CRATEDB_USER, CRATEDB_PASSWORD), data='INSERT INTO iot_events (event_id, device_id, status) VALUES (?, ?, ?)', params=(msg.topic, msg.topic, 'test'))
		

	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message

	client.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT, MQTT_BROKER_TIMEOUT)
	client.loop_forever()