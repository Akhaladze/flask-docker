from iot import celery
import paho.mqtt.client as mqtt

@celery.task
def getShellyStatuses():
    def on_connect(client, userdata, flags, rc):
        print("Connected to MQTT broker")
        client.subscribe("#")  # Subscribe to all topics

    def on_message(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("192.168.88.229", 1883, 60)
    client.loop_forever()
