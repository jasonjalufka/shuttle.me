from init import ask
from flask_ask import Ask, request, statement, question, session
from views import tracker, preferences, display


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

#if prefs.json file is configured, do questions. if not, ask user to configure on webpage...


@ask.intent("BusQuantityIntent")
def bus_quantity_intent():
#    print preferences
    quantity = len(preferences.get('buses')[0])
    print ("quantity of buses: " + str(quantity))
    if quantity == 1:
        message = "There is " + str(quantity) + " bus running on your route at the moment..."
    elif quantity > 1:
        message = "There are " + str(quantity) + " buses running on your route at the moment..."
    else:
        message = "There are no buses running on your route at the moment..."

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
        if currentStop == 1:
            pluralMin = "minute"
        else:
            pluralMin = "minutes"
        cardMessage = ("Stop: " + currentStop +
                       "\nDistance: " + currentDistance +
                       "    \n" + audioToggle +
                       "    \n" + visualToggle)
        message = ("Current stop is set at " + currentStop +
                    "...Current distance is set to " +
                    currentDistance + pluralMin +
                    audioToggle + ", and " + visualToggle)
        return statement(message).simple_card(cardMessage)
    else:
        return statement("Configure all your settings first on the shuttle me configuration portal.")


@ask.intent("AudioOffIntent")
def audio_off_intent():
    if preferences['configuration'].get('isConfigured') == True:
        if preferences['audio'] == False:
            return statement("Audio toggle is already deactivated...")
        else:
            preferences['audio'] = False
            return statement("Audio toggle has been deactivated...")
    else:
        return statement("Configure all your settings first on the shuttle me configuration portal.")


@ask.intent("AudioOnIntent")
def audio_on_intent():
    if preferences['configuration'].get('isConfigured') == True:
        if preferences['audio'] == True:
            return statement("Audio toggle is already activated...")
        else:
            preferences['audio'] = True
            return statement("Audio toggle has been activated...")
    else:
        return statement("Configure all your settings first in the shuttle me configuration portal.")


@ask.intent("VisualOffIntent")
def visual_off_intent():
    if preferences['configuration'].get('isConfigured') == True:
        if preferences['visual'] == False:
            return statement("Visual toggle is already deactivated...")
        else:
            preferences['visual'] = False
            return statement("Visual toggle has been deactivated...")
    else:
        return statement("Configure all your settings first in the shuttle me configuration portal.")


@ask.intent("VisualOnIntent")
def visual_on_intent():
    if preferences['configuration'].get('isConfigured') == True:
        if preferences['visual'] == True:
            return statement("Visual Toggle is already activated...")
        else:
            preferences['visual'] = True
            return statement("Visual toggle has been activated...")
    else:
        return statement("Configure all your settings first in the shuttle me configuration portal.")


@ask.intent("TimeLeftIntent")
def time_left_intent():
    time_left = preferences["timeLeft"]
    if time_left == -1:
        return statement("All buses are currently past your stop and heading back to campus.")
    else:
        return statement("The bus will be arriving in about " + time_left + " minutes...")

@ask.session_ended
def session_ended():
    return "", 200