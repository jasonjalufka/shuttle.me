from flask import Flask
import flask
from doublemap import DoubleMap


app = Flask(__name__)

display = {}

tracker = DoubleMap('txstate')

for stopKey, stopValue in tracker.stops.iteritems():
    display.update({stopKey: stopValue["name"]})


@app.route('/')
def index():
    return flask.render_template("configure.html", data=display)
    # return flask.render_template("index.html", data=display)


@app.route('/getConfig', methods=['POST'])
def configure():
    print "Configuration Info:"
    stop = flask.request.form['bus-stops']
    distance = flask.request.form['distance']
    toggles = flask.request.form.getlist('check')
    if('audio' in toggles):
        audio = True
    else:
        audio = False

    if('visual' in toggles):
        visual = True
    else:
        visual = False

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


@app.route('/getStop', methods=['POST'])
def get_stop():
    stop = flask.request.form['bus-stops']
    print tracker.stops[int(stop)]
    return flask.render_template("temp.html", name=tracker.stops[int(stop)]["name"], lat=tracker.stops[int(stop)]["lat"], lon=tracker.stops[int(stop)]["lon"])


@app.route('/getTime', methods=['POST'])
def get_time():
    return "gotem"


if __name__ == '__main__':
    app.run()
