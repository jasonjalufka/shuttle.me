from flask import Flask, jsonify, render_template, request
import flask
from doublemap import DoubleMap
from functools import partial
import math
import requests
import json
import os

app = Flask(__name__)

# Load database into data variable
#SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
#db_url = os.path.join(SITE_ROOT, "db.json")
#data = json.load(open(db_url))

display = {}
tracker = DoubleMap('txstate')


# IGNORE THIS SECTION IT WILL BE MOVED LATER!!!!
stopLat = tracker.stop_info(38)["lat"]
stopLon = tracker.stop_info(38)["lon"]

fullPath = tracker.route_info(408)["path"]

# separate fullPath into coordinate lat, lon pairs
pairs = zip(fullPath[::2], fullPath[1::2])

# find coordinate closest to stop coordinate in route
dist = lambda s, d: (s[0]-d[0])**2+(s[1]-d[1])**2
coord = (stopLat, stopLon)
lastPair = min(pairs, key=partial(dist, coord))

# index of closest coordinate to stop
# tells us last coordinate to load
endLocationIndex = pairs.index(lastPair)

# this isn't right
skip = (endLocationIndex/23)

count = 0
locations = []
#locations = [pairs[0][0]]
#locations.append(pairs[0][1])

for pair in pairs[0:endLocationIndex:4]:
    test = str(pair[0]) + ", " + str(pair[1])
    locations.append(test)
    #locations.append(pair[0])
    #locations.append(pair[1])
#locations.append(coord[0])
#locations.append(coord[1])


#print locations
#print len(locations)
url = 'https://www.mapquestapi.com/directions/v2/route?json={"locations":["%s"]}&outFormat=json&key=tAY5u0ki3CMdkv7GoGxT7ctvXEaKCSX9' % '", "'.join(map(str, locations))
mapquest_response = requests.get(url).json()
print mapquest_response
print url
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
        print "Configuration Info:"
        stop = flask.request.form['bus-stops']
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

        return flask.render_template("temp.html", name=tracker.stops[int(stop)]["name"],
                                     lat=tracker.stops[int(stop)]["lat"], lon=tracker.stops[int(stop)]["lon"])


@app.route('/_get_arrival_time')
def get_route():
    blancoRiver = 408
    shortPath = ()
    longPath = tracker.route_info(blancoRiver)["path"]

    url = 'https://www.mapquestapi.com/directions/v2/route?json={"locations":[]}&outFormat=json&key=KEY'


@app.errorhandler(404)
def page_not_found(err):
    return flask.render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
