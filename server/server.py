# -*- coding: utf-8 -*-
"""
    server.py
    ~~~~~~
"""
import eventlet
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_socketio import SocketIO
from pprint import pprint
import googlemaps
from threading import Thread
import os
from .DatabaseManager import DatabaseManager
eventlet.monkey_patch()

app = Flask(__name__, static_url_path="/static")
CORS(app)

# Generic configuration for the app.
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, "database.db"),
    DEBUG=True,
    SECRET_KEY="my-super-secret-key",
    MAPS_KEY="AIzaSyAqhytct605m66JtpY4grvk8D0n9fbQMV0"
))

# instantiate Google Maps client
gmaps = googlemaps.Client(key=app.config["MAPS_KEY"])

# get ref to the database
dbmgr = DatabaseManager(app.config["DATABASE"])

socketio = SocketIO(app)


def send_data(lat, lng, app_id, short_name, long_name, d_at):
    """ Save into the database and emits a new message
    over socket to the connected client. """
    data = {
        "lat": lat,
        "lng": lng,
        "downloaded_at": d_at,
        "app_id": app_id,
        "short_name": short_name,
        "long_name": long_name
    }
    # save new data into db
    dbmgr.save_download(lat, lng, app_id, short_name, long_name, d_at)
    # emit the new data
    socketio.emit("data", {"payload": data}, namespace="/sio")


@app.route("/")
def index():
    """Sends the static index.html page.
    Also, it injects the MAPS_KEY needed for the Google Maps API calls."""
    return render_template("index.html", api_key=app.config["MAPS_KEY"])


@app.route("/stats/byCountry")
def byCountry():
    """ Returns statistics about the number of download for each country. """
    # read from db
    results = dbmgr.get_data_by_country()
    # send data via json
    return jsonify({"status": "OK", "results": results})


@app.route("/stats/byTime")
def byTime():
    """ Returns statistics about the number of download for during a day. """
    # read from db
    results = dbmgr.get_data_by_time()
    # send data via json
    return jsonify({"status": "OK", "results": results})


@app.route("/stats/history")
def history():
    """ Returns statistics about the number
    of download since the beginning. """
    # read from db
    results = dbmgr.get_history()
    # send data via json
    return jsonify({"status": "OK", "results": results})


@app.route("/getAllDownloads", methods=["GET"])
def readJson():
    """ Returns all downloads in order to
    place markers onto the Google Map view. """
    # read from db
    results = dbmgr.get_all_downloads()
    # send data via json
    return jsonify({"status": "OK", "results": results})


@app.route("/new", methods=["POST"])
def newData():
    """ Routes needed for getting new data from the clients.
    Before to save the date, it checks if the data is `reliable`, using
    the Google Maps service, in particular doing a reverse geocode.
    This is needed because of the random values for longitude and latitude
    got by the generator.py script.
    If geo-data is valid a new thread gets spawned in order to save and
    send the socket.io message in background. """
    content = request.json
    reverse_geocode_result = gmaps.reverse_geocode(
        (content["lat"], content["lng"]),
        result_type='country')

    res = None
    if len(reverse_geocode_result) > 0:
        short_name, long_name = \
            reverse_geocode_result[0]["address_components"][0]["short_name"], \
            reverse_geocode_result[0]["address_components"][0]["long_name"]

        # create a new thread for background ops
        thread = Thread(target=send_data, args=(
                        content["lat"],
                        content["lng"],
                        content["app_id"],
                        short_name,
                        long_name,
                        content["downloaded_at"]
                        ))

        thread.daemon = True
        thread.start()
        res = "OK"
    else:
        pprint("Geo-data not valid")
        res = "NO"

    return res


@socketio.on('connect', namespace="/sio")
def test_connect():
    """ Debug only - Get notified when a
    client connects to the web socket."""
    print('Client connected')


@socketio.on('disconnect', namespace="/sio")
def test_disconnect():
    """ Debug only - Get notified when a
    client disconnects to the web socket."""
    print('Client disconnected')


socketio.run(app)
