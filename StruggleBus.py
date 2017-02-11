from flask import Flask
import flask
from doublemap import DoubleMap


app = Flask(__name__)

display = {}

tracker = DoubleMap('txstate')


for stopkey, stopvalue in tracker.stops.iteritems():
    b = {stopkey: stopvalue["name"]}
    display.update(b)


@app.route('/')
def index():
    return flask.render_template("index.html", data=display)


@app.route('/getStop', methods=['POST'])
def get_stop():
    stop = flask.request.form['stop']
    print tracker.stops[int(stop)]
    return flask.render_template("temp.html", name = tracker.stops[int(stop)]["name"], lat = tracker.stops[int(stop)]["lat"], lon = tracker.stops[int(stop)]["lon"])


@app.route('/getTime', methods=['POST'])
def get_time():
    return "gotem"
if __name__ == '__main__':
    app.run()
