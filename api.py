from views import tracker, preferences
from flask import jsonify, request, redirect, url_for, abort
import flask
from math import ceil
import requests
from functools import partial
from init import app

closest_bus = {}

@app.route('/_update_preferences', methods=['POST'])
def update_preferences():
    data = request.get_json()

@app.route('/_get_arrival_time', methods=['GET', 'POST'])
def get_route():

    #get list of running buses from ajax
    buses = request.args.getlist('buses[]')

    if not closest_bus:
        abort(401)
    else:

        locations = []

        print len(buses)
        print buses[0]

        stop = preferences.get("stop")
        print "STOP"
        print stop
        route = preferences.get("route")
        print route


        start = tracker.route_info(route)["stops"][0]
        print start
        startLat = tracker.stop_info(int(start))["lat"]
        print startLat

        startLon = tracker.stop_info(int(start))["lon"]
        print startLon

        stopLat = tracker.stop_info(int(stop))["lat"]

        stopLon = tracker.stop_info(int(stop))["lon"]
        print stopLon

        fullPath = tracker.route_info(route)["path"]

        # separate fullPath into coordinate lat, lon pairs
        pairs = zip(fullPath[::2], fullPath[1::2])
        print "Pairs"
        print len(pairs)

        # find coordinate closest to stop coordinate in route
        dist = lambda s, d: (s[0] - d[0]) ** 2 + (s[1] - d[1]) ** 2
        startCoord = (startLat, startLon)
        stopCoord = (stopLat, stopLon)
        firstPair = min(pairs, key=partial(dist, startCoord))
        lastPair = min(pairs, key=partial(dist, stopCoord))

        # index of closest coordinate to stop
        # tells us last coordinate to load
        startLocationIndex = pairs.index(firstPair)
        print startLocationIndex
        endLocationIndex = pairs.index(lastPair)
        print endLocationIndex
        print "TakeSpread:"
        locationGenerator = takespread(range(startLocationIndex-endLocationIndex), 23)
        # locationGenerator = takespread(range(1, len(pairs)-1), 23)
        for i in locationGenerator:
            test = str(pairs[i][0]) + ", " + str(pairs[i][1])
            locations.append(test)

        # insert starting location location as first location element
        locations.append(str(stopLat) + ", " + str(stopLon))
        # insert user
        locations.insert(0, str(startLat) + ", " + str(startLon))
        # locations.insert(str(pairs[endLocationIndex][0]) + ", " + str(pairs[endLocationIndex][1]))

        print locations[0]
        print locations

        url = 'https://www.mapquestapi.com/directions/v2/route?json={"locations":["%s"]}&timeType=1&useTraffic=true\
        &outFormat=json&key=tAY5u0ki3CMdkv7GoGxT7ctvXEaKCSX9' % '", "'.join(map(str, locations))

        response = requests.get(url).json()
        print response
            # return flask.redirect(url_for('/'))
        return jsonify(response)

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

    if closest_bus:
        closest_bus["last_stop"] = tracker.bus_info(closest_bus.keys[0])["laststop"]
        if closest_bus["last_stop"] not in preferences["route_stops"]:
            closest_bus.clear()

    for bus in buses:
        last_stop = tracker.bus_info(bus)["laststop"]
        # the following will go through if the bus hasn't passed user stop
        if last_stop in preferences["route_stops"]:
            bus_coming = True
            index = preferences["route_stops"].index(last_stop)
            bus_obj = {bus: {"last_stop": last_stop, "index": index}}
            bus_info.update(bus_obj)

    # there is a bus somewhere at UAC through user stop
    if bus_coming:
        # there was a previous closest_bus
        if not closest_bus:
            # assign the first bus as the closest bus
            closest_bus.update(bus_info[bus_info.keys[0]])
            for bus in bus_info:
                if closest_bus["last_stop"] < bus["last_stop"]:
                    closest_bus.clear()
                    closest_bus.update(bus)

    return




