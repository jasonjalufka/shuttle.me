from views import tracker, preferences
from flask import jsonify, request, redirect, url_for, abort
import flask
from math import ceil
import requests
from functools import partial
from init import app

closest_bus = {}
closest_buses = []

# Moved these here because it only needs to be retrieved once
#print preferences["stop"]
# print preferences.get("stop")
# stopLat = tracker.stop_info(int(preferences.get("stop")))["lat"]
# stopLon = tracker.stop_info(int(preferences.get("stop")))["lon"]
# fullPath = tracker.route_info(preferences["route"])["path"]
# pairs = zip(fullPath[::2], fullPath[1::2])


@app.route('/_update_preferences', methods=['POST'])
def update_preferences():
    data = request.get_json()

@app.route('/_get_arrival_time', methods=['GET', 'POST'])
def get_route():

    #get list of running buses from ajax
    buses = request.args.getlist('buses[]')
    get_closest_bus(buses)
    if not closest_buses:
        print "is this why"
        abort(401)
    else:
        # we have a bus coming!
        print "we have a bus coming!"

        #locations = []

        stop = preferences.get("stop")
        route = preferences.get("route")

        response = {}
        # get bus lat and lon
        print "closest buses!"
        #print closest_bus["id"]
        #print closest_buses

        response["number"]=len(closest_buses)

        for bus in closest_buses:
            bus["formattedTime"] = get_eta(bus)

        response["buses"] = closest_buses
        print response
        #startLat = tracker.bus_info(int(closest_bus["id"]))["lat"]
        #print startLat

        #startLon = tracker.bus_info(int(closest_bus["id"]))["lon"]
        #print startLon

        # last stop lat lon


        # separate fullPath into coordinate lat, lon pairs
        #print "Pairs"
        #print len(pairs)

        # find coordinate closest to stop coordinate in route
        # dist = lambda s, d: (s[0] - d[0]) ** 2 + (s[1] - d[1]) ** 2
        # startCoord = (startLat, startLon)
        # stopCoord = (stopLat, stopLon)
        # firstPair = min(pairs, key=partial(dist, startCoord))
        # lastPair = min(pairs, key=partial(dist, stopCoord))

        # index of closest coordinate to stop
        # tells us last coordinate to load
        #startLocationIndex = pairs.index(firstPair)
        #print startLocationIndex
        #endLocationIndex = pairs.index(lastPair)
        #print endLocationIndex
        #print "TakeSpread:"
        #locationGenerator = takespread(range(startLocationIndex,endLocationIndex), 23)
        # locationGenerator = takespread(range(1, len(pairs)-1), 23)
        # for i in locationGenerator:
        #     test = str(pairs[i][0]) + ", " + str(pairs[i][1])
        #     locations.append(test)

        # insert starting location location as first location element
        # locations.append(str(stopLat) + ", " + str(stopLon))
        # insert user
        #locations.insert(0, str(startLat) + ", " + str(startLon))
        # locations.insert(str(pairs[endLocationIndex][0]) + ", " + str(pairs[endLocationIndex][1]))

        #print locations[0]
        #print locations

        #url = 'https://www.mapquestapi.com/directions/v2/route?json={"locations":["%s"]}&timeType=1&useTraffic=true\
        #&outFormat=json&key=tAY5u0ki3CMdkv7GoGxT7ctvXEaKCSX9' % '", "'.join(map(str, locations))

        #response = requests.get(url).json()
            # return flask.redirect(url_for('/'))
        return jsonify(response)


# function that gets the ETA for each bus heading your way

def get_eta(bus):
    print bus
    stopLat = tracker.stop_info(int(preferences.get("stop")))["lat"]
    stopLon = tracker.stop_info(int(preferences.get("stop")))["lon"]
    fullPath = tracker.route_info(preferences["route"])["path"]
    pairs = zip(fullPath[::2], fullPath[1::2])
    pairs = pairs[0:-10]
    locations = []

    startLat = tracker.bus_info(int(bus["id"]))["lat"]
    startLon = tracker.bus_info(int(bus["id"]))["lon"]

    dist = lambda s, d: (s[0] - d[0]) ** 2 + (s[1] - d[1]) ** 2
    startCoord = (startLat, startLon)
    stopCoord = (stopLat, stopLon)

    print "startCord"
    print startCoord
    firstPair = min(pairs, key=partial(dist, startCoord))
    print "first pair"
    print firstPair
    lastPair = min(pairs, key=partial(dist, stopCoord))

    startLocationIndex = pairs.index(firstPair)
    endLocationIndex = pairs.index(lastPair)

    # check to see the range before trying to split it up
    if (endLocationIndex - startLocationIndex) < 25:
        print "im pretty close"
        # do this
        for i in range(startLocationIndex, endLocationIndex):
            test = str(pairs[i][0]) + ", " + str(pairs[i][1])
            locations.append(test)
    else:
        print "i'm pretty far"
        locationGenerator = takespread(range(startLocationIndex, endLocationIndex), 23)
        for i in locationGenerator:
            test = str(pairs[i][0]) + ", " + str(pairs[i][1])
            locations.append(test)
        locations.append(str(stopLat) + ", " + str(stopLon))
        locations.insert(0, str(startLat) + ", " + str(startLon))
    print "location length"
    print len(locations)
    url = 'https://www.mapquestapi.com/directions/v2/route?json={"locations":["%s"]}&timeType=1&useTraffic=true\
            &outFormat=json&key=tAY5u0ki3CMdkv7GoGxT7ctvXEaKCSX9' % '", "'.join(map(str, locations))

    print "URL"
    print url
    urlresponse = requests.get(url).json()
    print "url response"
    print urlresponse
    print urlresponse["route"]["formattedTime"]
    return urlresponse["route"]["formattedTime"]


# choose num elements from sequence distributed as evenly as possible
def takespread(sequence, num):
    length = float(len(sequence))
    temp = []
    for i in range(num):
        yield sequence[int(ceil(i * length / num))]


def get_closest_bus(buses):
    bus_info = {}

    # will change value if there's a bus soon to come
    bus_coming = False

    if closest_buses:
        for bus in closest_buses:
            bus["last_stop"] = tracker.bus_info(bus["id"]["lastStop"])
            if bus["last_stop"] not in preferences["route_stops"]:
                closest_buses.remove(bus)

    if closest_bus:
        closest_bus["last_stop"] = tracker.bus_info(closest_bus["id"])["lastStop"]
        if closest_bus["last_stop"] not in preferences["route_stops"]:
            closest_bus.clear()

    for bus in buses:
        last_stop = tracker.bus_info(int(bus))["lastStop"]
        # the following will go through if the bus hasn't passed user stop
        if last_stop in preferences["route_stops"]:
            bus_coming = True
            index = preferences["route_stops"].index(last_stop)
            bus_obj = {bus: {"last_stop": last_stop, "index": index, "id":bus}}
            #print bus_obj
            bus_info.update(bus_obj)

            closest_buses.append(bus_obj[bus])

    # there is a bus somewhere at UAC through user stop
    if bus_coming:
        # there was a previous closest_bus
        if not closest_bus:
            # assign the first bus as the closest bus
            closest_bus.update(bus_info[bus_info.keys()[0]])
            for key, bus in bus_info.iteritems():
                if closest_bus["index"] < bus["index"]:
                    closest_bus.clear()
                    closest_bus.update(bus)
                    #print closest_bus
    #print closest_bus
    return




