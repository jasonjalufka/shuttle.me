from init import app
import flask
from doublemap import DoubleMap

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
                                     lat=tracker.stops[int(stop)]["lat"], lon=tracker.stops[int(stop)]["lon"],
                                     route=tracker.routes[int(route)]["name"], bus_info=buses)


def get_buses(route):
    buses = []

    for busKey, busValue in tracker.buses.iteritems():
        if busValue["route"] == route:
            buses.append(busValue["name"])
    return buses


@app.errorhandler(404)
def page_not_found(err):
    return flask.render_template('404.html'), 404


