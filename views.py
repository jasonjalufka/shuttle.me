from init import app
import flask
from doublemap import DoubleMap
from flask import url_for
import json, os

#dictionary of stops to send to the front end
display = {}
preferences = {}
preferences['configuration'] = {'isConfigured': False}
tracker = DoubleMap('txstate')
validStops = [1, 2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 21, 24, 25, 26, 31, 32, 33, 34, 35, 37, 38, 39, 40, 41, 44]

for stopKey, stopValue in tracker.stops.iteritems():
    if stopKey in validStops:
        display.update({stopKey: stopValue["name"]})


resource_path = os.path.join(app.root_path, 'display.json')
with open(resource_path, "wb") as fo:
    json.dump(display, fo, indent=4)

with open(resource_path) as json_file:
    data = json.load(json_file)

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
        if not route or not buses:
            return flask.redirect(url_for('index'))

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

        #call get routestops: pass in route, stop
        route_stops = get_routestops(route, stop)

        information = {'stop': stop, 'route': route, 'distance': distance, 'audio': audio, 'visual': visual, 'buses': [buses]}
        preferences.update(information)
        preferences['route_stops'] = route_stops
        preferences['configuration'] = {'isConfigured': True}

        resource_path = os.path.join(app.root_path, 'prefs.json')
        with open(resource_path, "wb") as fo:
            json.dump(preferences, fo, indent=4)

        with open(resource_path) as json_file:
            data = json.load(json_file)

        return flask.render_template("dashboard.html", name=tracker.stops[int(stop)]["name"],
                                     lat=tracker.stops[int(stop)]["lat"], lon=tracker.stops[int(stop)]["lon"],
                                     route=tracker.routes[int(route)]["name"], bus_info=buses, info=information)


def get_buses(route):
    buses = []

    for busKey, busValue in tracker.buses.iteritems():
        if busValue["route"] == route:
            buses.append(busValue["name"])
    return buses


def get_routestops(route, userstop):
    # full list of stops in route
    stops = tracker.route_info(route)["stops"]

    # this array ignores stops after user's stop
    stopsToCheck = []

    # get the length of array of stops
    length = len(stops)

    # appends campus stop first
    stopsToCheck.append(stops[length-1])

    for stop in stops:
        # do not append stops after user stop
        if stop == userstop:
            break
        stopsToCheck.append(stop)
    return stopsToCheck


@app.errorhandler(404)
def page_not_found(err):
    return flask.render_template('404.html'), 404


