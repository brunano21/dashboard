# -*- coding: utf-8 -*-
"""
    generator.py
    ~~~~~~
    This program randomly creates geo-data and sends request
    to the running server, in order to emulate the upload on new data.
    The requests are generated in a random time,
    (from 1 second up to 5 seconds.)
"""
import json
import sched
import time
import random
import requests


s = sched.scheduler(time.time, time.sleep)
app_ids = ["IOS_ALERT", "IOS_MATE", "ANDROID_ALERT", "ANDROID_MATE"]
postUrl = "http://127.0.0.1:5000/new"
headers = {
    "content-type": "application/json"
}


def get_random_data():
    """ Generates data in order to be uploaded to the server
        Everything in here is calculated in a random way. """
    lng, lat = random.uniform(-180, 180), random.uniform(-90, 90)
    data = {
        "lng": lng,
        "lat": lat,
        "app_id": random.choice(app_ids),
        "downloaded_at": random.randint(1470614400000, 1495531190438)
    }
    print "Generated: ", data
    return data


def send_data():
    """ Makes the post request. For debugging, it print the response
        sent from the server. """
    response = requests.post(
        postUrl, data=json.dumps(get_random_data()), headers=headers)
    print response.text


def loop(sc):
    """ Simple loop that use a scheduler to run the send_data() func,
        every random (1 up to 5) seconds. """
    send_data()
    s.enter(random.randint(1, 5), 1, loop, (sc,))


s.enter(random.randint(1, 5), 1, loop, (s,))
s.run()
