from init import ask, app
from flask import Flask, render_template
from flask_ask import Ask, request, statement, question, session
from views import tracker, preferences, display
import json, os


@ask.launch
def start_skill():
    current = len(tracker.buses)
    question_text = "What would you like me to do?"
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
    if preferences['configuration'].get('isConfigured') == True:
        if preferences['audio'] == True:
            audioToggle = "audio toggle is on"
        else:
            audioToggle = "audio toggle is off"

        if preferences['visual'] == True:
            visualToggle = "visual toggle is on"
        else:
            visualToggle = "visual toggle is off"

        stopNum = preferences['stop']
        currentDistance = preferences['distance']  # how to access the db.json elements
        print ("STOPNUM: " + stopNum)
        currentStop = display[str(stopNum)]
        return statement("Current stop is set to " + currentStop +
                         "...Current distance is set to " + currentDistance + " minutes..." +
                         audioToggle + ",and" + visualToggle)
    else:
        return statement("Configure first, then come back")

@ask.session_ended
def session_ended():
    return "", 200