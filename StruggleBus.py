from flask import Flask
import flask
from doublemap import DoubleMap
import json
import os

app = Flask(__name__)

# if os.path.exists('db.json'):
#     userPreferences = json.load(open('db.json', 'r', encoding='UTF8'))

display = {}
userPreferences = {}

# Load user preferences from json file
# with open('db.json') as f:
#     userPreferences = json.load(f)

tracker = DoubleMap('txstate')

for stopKey, stopValue in tracker.stops.iteritems():
    display.update({stopKey: stopValue["name"]})


@app.route('/')
def index():
    return flask.render_template("index.html")
    # return flask.render_template("configure.html", data=display)


@app.route('/configure', methods=['GET', 'POST'])
def configure():
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

        userPreferences.update({'Stop': stop, 'Distance': distance, 'Audio': audio, 'Visual': visual})

        print "Distance: " + distance + " minutes"
        if audio:
            print "audio toggle is on"
        else:
            print "audio toggle is off"

        if visual:
            print "visual toggle is on"
        else:
            print "visual toggle is off"

        print "Selected Stop: " + tracker.stops[int(stop)]["name"]

        return flask.render_template("temp.html", name=tracker.stops[int(stop)]["name"],
                                     lat=tracker.stops[int(stop)]["lat"], lon=tracker.stops[int(stop)]["lon"])
    else:
        return flask.render_template("configure.html", data=display)


@app.route('/getStop', methods=['POST'])
def get_stop():
    stop = flask.request.form['bus-stops']
    print tracker.stops[int(stop)]
    return flask.render_template("temp.html", name=tracker.stops[int(stop)]["name"], lat=tracker.stops[int(stop)]["lat"], lon=tracker.stops[int(stop)]["lon"])


@app.route('/getTime', methods=['POST'])
def get_time():
    return "gotem"


@app.errorhandler(404)
def page_not_found(err):
    return flask.render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
