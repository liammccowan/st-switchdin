#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import random
import time
import pickle

# seed rng
random.seed()

# set up mqtt client
mqttc = mqtt.Client(client_id = "generator")
mqttc.connect(host = "localhost", port = 1883, keepalive = 31)

# loop indefinitely to generate numbers and publish them
while (True):
    # generate random integer
    r = random.randrange(1, 101, 1)

    # create playload by packing tuple, use pickle for serialization
    payload = pickle.dumps((r, time.time()))

    # publish payload
    mqttc.publish("st/rng", payload)

    # sleep for random time in seconds between 1 and 30
    t = random.randrange(1, 31, 1)
    time.sleep(t)

