from init import app
import flask
from doublemap import DoubleMap
from flask import url_for
import json, os

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



        information = {'stop': stop, 'route': route, 'distance': distance, 'audio': audio, 'visual': visual, 'buses': [buses]}
        preferences.update(information)
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


@app.errorhandler(404)
def page_not_found(err):
    return flask.render_template('404.html'), 404


