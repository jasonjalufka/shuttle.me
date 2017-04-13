from views import tracker, preferences
from flask import jsonify
import requests
from functools import partial
from init import app


@app.route('/_get_arrival_time', methods=['GET'])
def get_route():

    print "IN GET ARRIVAL TIME AJAX THING"

    print len(preferences["buses"])
    print preferences["buses"][0]
    stop = preferences.get("stop")
    print stop
    route = preferences.get("route")
    print route
    stopLat = tracker.stop_info(int(stop))["lat"]
    print stopLat
    stopLon = tracker.stop_info(int(stop))["lon"]
    print stopLon

    fullPath = tracker.route_info(route)["path"]

    # separate fullPath into coordinate lat, lon pairs
    pairs = zip(fullPath[::2], fullPath[1::2])

    # find coordinate closest to stop coordinate in route
    dist = lambda s, d: (s[0] - d[0]) ** 2 + (s[1] - d[1]) ** 2
    coord = (stopLat, stopLon)
    lastPair = min(pairs, key=partial(dist, coord))

    # index of closest coordinate to stop
    # tells us last coordinate to load
    endLocationIndex = pairs.index(lastPair)
    print "ENDLOCATIONINDEX"
    print endLocationIndex
    # this isn't right
    skip = (endLocationIndex / 23)
    print "SKIP"
    print skip
    count = 0
    locations = []

    for pair in pairs[0:endLocationIndex:4]:
        test = str(pair[0]) + ", " + str(pair[1])
        locations.append(test)
    print "LOCATIONS LENGTH"
    print len(locations)

    locations.pop(8)
    locations.pop(9)
    url = 'https://www.mapquestapi.com/directions/v2/route?json={"locations":["%s"]}&timeType=1&useTraffic=true\
    &outFormat=json&key=tAY5u0ki3CMdkv7GoGxT7ctvXEaKCSX9' % '", "'.join(map(str, locations))

    return jsonify(requests.get(url).json())
