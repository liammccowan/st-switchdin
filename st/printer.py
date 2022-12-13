#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import pickle

# callback for when client connects to server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " +  str(rc))
    client.subscribe("st/avg")

# callback for when message is received
def on_message(client, userdata, msg):
    # use pickle to deserialize payload, unpack tuple
    one, five, thirty = pickle.loads(msg.payload)

    # print averages
    print("| One minute average: {0:.2f}".format(one), \
        "| Five minute average: {0:.2f}".format(five), \
        "| Thirty minute average: {0:.2f} |".format(thirty))

# set up mqtt client
mqttc = mqtt.Client(client_id = "printer")
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect(host = "localhost", port = 1883, keepalive = 31)

mqttc.loop_forever()