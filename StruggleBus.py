from flask import Flask, jsonify, render_template, request
import flask
from doublemap import DoubleMap
import json
import os

app = Flask(__name__)

display = {}

tracker = DoubleMap('txstate')

# routeNumber = 447
# shortPath = []
# formattedLongPath = []
# locations = []
# longPath = tracker.route_info(routeNumber)["path"]
# print "LONG PATH LIST"
# print longPath
# for point in longPath:
#     formattedLongPath.append(str(point)[:-3])
# # formattedLongPath = ["%.3f" % point for point in longPath]
# # print formattedLongPath
# print "FORMATTED PATH LIST"
# print formattedLongPath
# total = len(longPath)/2
# skip = (total/23)*2
#
# stopLat = tracker.stop_info(16)["lat"]
# stopLon = tracker.stop_info(16)["lon"]
#
# lat = str(stopLat)[:-3]
# lon = str(stopLon)[:-3]
# print lat
# print lon
#
# # Find user's stop along route path in order to shorten the amount of data
# # If stop is found along path, stopIndex will be used to determine how many times next for loop will run
# stopIndex = 0
# for point in range(0, len(formattedLongPath), 2):
#     if formattedLongPath[point] == lat:
#         if formattedLongPath[point + 1] == lon:
#             print "Stop found at %s, %s\n Stop index: %d" % (lat, lon, stopIndex)
#             lastLocation = "%s, %s" % (lat, lon)
#             break
#     stopIndex += 2
#
#
# print skip
# for i in range(0, len(longPath)-1, skip):
#     if longPath[i] == stopLat:
#         print "found the stop dot"
#         break
#     shortPath.append(longPath[i])
#     shortPath.append(longPath[i+1])
#
# shortPath.append(longPath[(total * 2) - 2])
# shortPath.append(longPath[(total*2)-1])
#
# print len(shortPath)/2


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


@app.route('/_get_route')
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
