from flask import Flask, jsonify, render_template, request
import flask
from doublemap import DoubleMap
import json
import os

app = Flask(__name__)

display = {}

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


# @app.route('/_request_route')
# def request_route():

@app.errorhandler(404)
def page_not_found(err):
    return flask.render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
