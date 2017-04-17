from init import ask, app
from flask import Flask, render_template
from flask_ask import Ask, request, statement, question, session
from views import tracker, preferences, display
from init import app
import json, os


#current number of shuttles running
current = len(tracker.buses)

@ask.launch
def start_skill():
    if preferences['configuration'].get('isConfigured') == True:
        welcome = "Welcome to Shuttle Me..."
        question_text = "What would you like me to do?"
        return question(welcome + "There are " + str(current) + "buses running at the moment..." + question_text)
    else:
        return statement("Configure your settings first so I can get your bus information.")



#navigation for yes or no. 'Intent' is input from user
#utterance is the way that user says the intent
#@ask.intent("StopsIntent")
#def stops

#if prefs.json file is configured, do questions. if not, ask user to configure on webpage...

@ask.intent("YesIntent")
def yes_intent():
    message = "ok"
    return statement(message)

@ask.intent("BusQuantityIntent")
def bus_quantity_intent():
    len(preferences["buses"]) #need to get the number of buses running on current selected route
#    preferences[len('buses')]
    message = "There are " + str(current) + " buses running on your route at the moment..." #revert back to default func if errors.
    return statement(message)

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
        currentDistance = preferences['distance']
        print ("STOPNUM: " + stopNum)
        currentStop = display[int(stopNum)]
        cardMessage = ("Stop: " + currentStop +
                       "\nDistance: " + currentDistance +
                       "    \n" + audioToggle +
                       "    \n" + visualToggle)
        message = ("Current stop is set at " + currentStop +
                    "...Current distance is set to " +
                    currentDistance + " minutes... " +
                    audioToggle + ", and " + visualToggle)
        return statement(message).simple_card(cardMessage)
    else:
        return statement("Configure your settings first so I can get your bus information.")

@ask.intent("SetConfigurationIntent")
def set_configuration_intent():

    return statement("SET CONFIGURATION")

@ask.intent("TimeLeftIntent")
def alert_intent():
    timeLeft = preferences["timeLeft"]
    if timeLeft == -1:
        return statement("All buses are currently past your stop and heading back to campus.")
    else:
        return statement("The bus will be arriving in about " + timeLeft)

@ask.session_ended
def session_ended():
    return "", 200