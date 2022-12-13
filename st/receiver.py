#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import pickle
from collections import deque

# maintains a rolling average over the window provided on intialization,
# window to be provided in seconds
class RollingAverage:
    def __init__(self, window):
        self.window = window
        self.count = 0
        self.total = 0
        self.val_deque = deque()
    
    # updates and returns rolling average
    def average(self, val, val_time):
        # always add new value to deque
        self.val_deque.appendleft((val, val_time))

        # update count and total
        self.count += 1
        self.total += val

        # now work backwards removing all no longer in window
        for i in reversed(range(len(self.val_deque))):
            # check if value is no longer in window
            if self.val_deque[i][1] < val_time - self.window:
                # if it is, pop it from deque and adjust count and total
                val_removed, _ = self.val_deque.pop()
                self.count -= 1
                self.total -= val_removed
            else:
                # as values are added in chronological order,
                # we can break as soon as we find one that is in the window
                break
        
        # now calculate average and return
        return self.total / self.count
        
# initialize rolling averages
one_minute = RollingAverage(60)
five_minutes = RollingAverage(300)
thirty_minutes = RollingAverage(1800)

# callback for when client connects to server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("st/rng")

# callback for when a message is received
def on_message(client, userdata, msg):
    # use pickle for deserialization of payload, unpack tuple
    val, val_time = pickle.loads(msg.payload)

    # update rolling averages
    one_minute_average = one_minute.average(val, val_time)
    five_minute_average = five_minutes.average(val, val_time)
    thirty_minute_average = thirty_minutes.average(val, val_time)

    # create tuple of averages to be used in payload
    averages = (one_minute_average, five_minute_average, thirty_minute_average)

    # serialize payload with pickle
    payload = pickle.dumps(averages)

    # publish averages
    mqttc.publish("st/avg", payload)

# set up mqtt client
mqttc = mqtt.Client(client_id = "receiver")
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect(host = "localhost", port = 1883, keepalive = 31)

mqttc.loop_forever()
