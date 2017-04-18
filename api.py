from views import tracker, preferences
from flask import jsonify, request, redirect, url_for, abort
import flask
from math import ceil
import requests, json
from functools import partial
from init import app

closest_bus = {}
closest_buses = []



@app.route('/_update_preferences', methods=['POST'])
def update_preferences():
    data = request.get_json()

@app.route('/_get_arrival_time', methods=['GET'])
def get_route():
    print "called in get arrival time"
    del closest_buses[:]

    #get list of running buses from ajax
    buses = request.args.getlist('buses[]')
    print "was i able to get the buses?"
    bus_on_way = get_closest_bus(buses)
    #bus_on_way = False
    print "did this getclosestbus function upset it?"
    if not bus_on_way:
        print "is this why"
        return "error"
    else:
        # we have a bus coming!
        print "we have a bus coming!"
        stop = preferences.get("stop")
        route = preferences.get("route")

        response = {}
        # get bus lat and lon
        print "closest buses!"
        print closest_buses

        response["number"]=len(closest_buses)

        for bus in closest_buses:
            bus["formattedTime"] = get_eta(bus)

        response["buses"] = closest_buses
        print response

        return jsonify(response)


# function that gets the ETA for each bus heading your way

def get_eta(bus):
    print bus
    stopLat = tracker.stop_info(int(preferences.get("stop")))["lat"]
    stopLon = tracker.stop_info(int(preferences.get("stop")))["lon"]
    fullPath = tracker.route_info(preferences["route"])["path"]
    pairs = zip(fullPath[::2], fullPath[1::2])
    pairs = pairs[0:-15]
    locations = []

    startLat = tracker.bus_info(int(bus["id"]))["lat"]
    startLon = tracker.bus_info(int(bus["id"]))["lon"]

    dist = lambda s, d: (s[0] - d[0]) ** 2 + (s[1] - d[1]) ** 2
    startCoord = (startLat, startLon)
    stopCoord = (stopLat, stopLon)
    lastPair = min(pairs, key=partial(dist, stopCoord))
    endLocationIndex = pairs.index(lastPair)
    print "startCord"
    print startCoord
    firstPair = min(pairs, key=partial(dist, startCoord))
    print "first pair"
    print firstPair

    startLocationIndex = pairs.index(firstPair)
    print "indices"
    print startLocationIndex
    print endLocationIndex

    if startLocationIndex > endLocationIndex:
        return -1
    else:
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
        print locations
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

    return bus_coming




