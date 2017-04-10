from flask import Flask, render_template
import flask
from doublemap import DoubleMap
from flask_ask import Ask, request, statement, question, session
import logging
import json
import os


app = Flask(__name__)
ask = Ask(app, "/")
tracker = DoubleMap('txstate')

display = {}
db = {}


for stopKey, stopValue in tracker.stops.iteritems():
    display.update({stopKey: stopValue["name"]})


db['stops'] = []

for stopKey, stopValue in tracker.stops.iteritems():
    #store stop ID's and stop names in JSON format in db.json
    db['stops'].append({
        'stopID': stopKey,
        'stopName': stopValue["name"]
    })

    with open("/Users/ryanjalufka/PycharmProjects/strugglebus/db.json", "wb") as fo:
        json.dump(db, fo, indent=4)

    with open("/Users/ryanjalufka/PycharmProjects/strugglebus/db.json") as json_file:
        data = json.load(json_file)
        for key in db['stops']:
            print("STOP NAME: " + key['stopName']) + ("\tSTOP ID: " + (str(key['stopID'])))

@app.route('/')
def index():
    # retrieve the current amount of buses running
    current = len(tracker.buses)
    print current

    # return flask.render_template("configure.html", data=display)
    return flask.render_template("index.html", current=current)

@app.route('/configure', methods=['GET', 'POST'])
def configure():
    db['prefs'] = []

    if flask.request.method == 'POST':
        print "Configuration Info:"
        stop = flask.request.form['bus-stops']
        distance = flask.request.form['distance']
        toggles = flask.request.form.getlist('check')
        if 'audio' in toggles:
            audio =True
        else:
            audio = False

        if 'visual' in toggles:
            visual = True
        else:
            visual = False

        db['prefs'].append({
            'audio': audio,
            'visual': visual,
            'stop': stop,
            'distance': distance
        })

        with open("/Users/ryanjalufka/PycharmProjects/strugglebus/db.json", "wb") as fo:
            json.dump(db, fo, indent=4)

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


######################################################
# Alexa flask-ask section #
######################################################



@ask.launch
def start_skill():
    current = len(tracker.buses)
    question_text = render_template('welcome')
    return question("There are " + str(current) + " busses running at the moment" + question_text)


#navigation for yes or no. 'Intent' is input from user
#utterance is the way that user says the intent
#@ask.intent("StopsIntent")
#def stops

#if json file is populated, do questions. if not, ask user to say a specific route.
#maybe use session.attributes to keep data relevant for the current user.

@ask.intent("YesIntent")
def yes_intent():
    current = "your current stop is " + tracker.stops[int()]["name"]
    return statement(current)


@ask.intent("BusQuantityIntent")
def bus_quantity_intent():
    current = len(tracker.buses)
    return statement("There are " + str(current) + " busses running at the moment")


@ask.intent("BusIDIntent")
def bus_ID_intent():
    bus_message = "Which bus number's ETA would you like?"
    return question(bus_message)


@ask.session_ended
def session_ended():
    return "", 200


######################################################

if __name__ == '__main__':
    app.run(debug=True)
    logging.getLogger('flask_ask').setLevel(logging.DEBUG)
