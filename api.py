from views import tracker, preferences
from flask import jsonify, request, redirect, url_for
import flask
from math import ceil
import requests
from functools import partial
from init import app

@app.route('/_update_preferences', methods=['POST'])
def update_preferences():
    data = request.get_json()

@app.route('/_get_arrival_time', methods=['GET', 'POST'])
def get_route():

    locations = []

    #get list of running buses from ajax
    buses = request.args.getlist('buses[]')


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
