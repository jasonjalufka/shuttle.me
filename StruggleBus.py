from flask import Flask, jsonify, render_template, request
from flask_ask import Ask, request, statement, question, session
import flask
import logging
from doublemap import DoubleMap
from functools import partial
import math
import requests
import json
import os

app = Flask(__name__)
tracker = DoubleMap('txstate')
ask = Ask(app, "/")

# Load database into data variable
#SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
#db_url = os.path.join(SITE_ROOT, "db.json")
#data = json.load(open(db_url))

display = {}
preferences = {}
tracker = DoubleMap('txstate')


for stopKey, stopValue in tracker.stops.iteritems():
    display.update({stopKey: stopValue["name"]})


@app.route('/')
def index():
    # retrieve the current amount of buses running
    current = len(tracker.buses)
    return flask.render_template("index.html", current=current)


@app.route('/configure', methods=['GET'])
def configure():
        return flask.render_template("configure.html", data=display)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if flask.request.method == 'POST':

        stop = flask.request.form['bus-stops']
        route = tracker.get_route(int(stop))
        buses = get_buses(route)
        distance = flask.request.form['distance']
        toggles = flask.request.form.getlist('check')
        if 'audio' in toggles:
            audio = True
        else:
            audio = False

        if 'visual' in toggles:
            visual = True
        else:
            visual = False

        information = {'stop': stop, 'route': route, 'distance': distance, 'audio': audio, 'visual': visual, 'buses': buses}
        preferences.update(information)

        return flask.render_template("temp.html", name=tracker.stops[int(stop)]["name"],
                                     lat=tracker.stops[int(stop)]["lat"], lon=tracker.stops[int(stop)]["lon"],\
                                     route=tracker.routes[int(route)]["name"], bus_info=buses)

def get_buses(route):
    buses = []

    for busKey, busValue in tracker.buses.iteritems():
        if busValue["route"] == route:
            buses.append(busValue["name"])
    return buses


@app.route('/_get_arrival_time', methods=['GET'])
def get_route():

    print "IN GET ARRIVAL TIME AJAX THING"

    print len(preferences["buses"])
    print preferences["buses"][0]
    stop = preferences.get("stop")
    print stop
    route = preferences.get("route")
    print route
    stopLat = tracker.stop_info(int(stop))["lat"]
    print stopLat
    stopLon = tracker.stop_info(int(stop))["lon"]
    print stopLon

    fullPath = tracker.route_info(route)["path"]

    # separate fullPath into coordinate lat, lon pairs
    pairs = zip(fullPath[::2], fullPath[1::2])

    # find coordinate closest to stop coordinate in route
    dist = lambda s, d: (s[0] - d[0]) ** 2 + (s[1] - d[1]) ** 2
    coord = (stopLat, stopLon)
    lastPair = min(pairs, key=partial(dist, coord))

    # index of closest coordinate to stop
    # tells us last coordinate to load
    endLocationIndex = pairs.index(lastPair)
    print "ENDLOCATIONINDEX"
    print endLocationIndex
    # this isn't right
    skip = (endLocationIndex / 23)
    print "SKIP"
    print skip
    count = 0
    locations = []

    for pair in pairs[0:endLocationIndex:4]:
        test = str(pair[0]) + ", " + str(pair[1])
        locations.append(test)
    print "LOCATIONS LENGTH"
    print len(locations)

    locations.pop(8)
    locations.pop(9)
    url = 'https://www.mapquestapi.com/directions/v2/route?json={"locations":["%s"]}&timeType=1\
    &outFormat=json&key=tAY5u0ki3CMdkv7GoGxT7ctvXEaKCSX9' % '", "'.join(map(str, locations))

    return jsonify(requests.get(url).json())

    # mapquest_response = requests.get(url).json()

    # print mapquest_response
    # print url

    # return jsonify(mapquest_response)


@app.errorhandler(404)
def page_not_found(err):
    return flask.render_template('404.html'), 404

### Alexa flask-ask section ###

@ask.launch
def start_skill():
    question_text = render_template('welcome')
    return question(question_text)

@ask.session_ended
def session_ended():
    return "session ended... ", 200

if __name__ == '__main__':
    app.run(debug=True)
    logging.getLogger('flask_ask').setLevel(logging.DEBUG)
