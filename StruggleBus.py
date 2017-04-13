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


db['stops'] = {}
db['configuration'] = {}
db['prefs'] = {}
db['configuration'].update({"isConfigured": False})

for stopKey, stopValue in tracker.stops.iteritems():
    #store stop ID's and stop names in JSON format in db.json
    db['stops'].update({
        stopKey: stopValue["name"]
    })
    resource_path = os.path.join(app.root_path, 'db.json')
    with open(resource_path, "wb") as fo:
        json.dump(db, fo, indent=4)

    with open(resource_path) as json_file:
        data = json.load(json_file)


@app.route('/')
def index():
    # retrieve the current amount of buses running
    current = len(tracker.buses)
    print current

    # return flask.render_template("configure.html", data=display)
    return flask.render_template("index.html", current=current)

@app.route('/configure', methods=['GET', 'POST'])
def configure():

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

        db['prefs'].update({
            'audio': audio,
            'visual': visual,
            'stop': stop,
            'distance': distance
        })
        db['configuration'].update({"isConfigured": True})

        with open(resource_path, "wb") as fo:
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
    current = "Never gonna give you up, never gonna let you down. Never gonna run around and desert you."
    return statement(current)

@ask.intent("ConfigurationInfoIntent")
def configuration_info_intent():
    if db['configuration'].get('isConfigured') == True:
        if db['prefs']['audio'] == True:
            audioToggle = "audio toggle is on"
        else:
            audioToggle = "audio toggle is off"

        if db['prefs']['visual'] == True:
            visualToggle = "visual toggle is on"
        else:
            visualToggle = "visual toggle is off"

        stopNum = db['prefs']['stop']
        currentDistance = db['prefs']['distance']  # how to access the db.json elements
        currentStop = db['stops'][int(stopNum)]
        return statement("Current stop is set to " + currentStop +
                         "...Current distance is set to " + currentDistance + " minutes..." +
                         audioToggle + ",and" + visualToggle)
    else:
        return statement("Configure first, then come back")

@ask.session_ended
def session_ended():
    return "", 200


######################################################

if __name__ == '__main__':
    app.run(debug=True)
    logging.getLogger('flask_ask').setLevel(logging.DEBUG)
