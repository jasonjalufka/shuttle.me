from views import tracker, preferences
from flask import jsonify, request
from math import ceil
import requests
from functools import partial
from init import app


@app.route('/_get_arrival_time', methods=['GET'])
def get_route():

    locations = []

    # buses = request.args.get('buses')
    # print buses[0]

    print len(preferences["buses"])
    print preferences["buses"][0]
    stop = preferences.get("stop")

    route = preferences.get("route")

    start = tracker.route_info(route)["stops"][0]

    startLat = tracker.stop_info(start)["lat"]

    startLon = tracker.stop_info(int(start))["lon"]

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
    coord = (stopLat, stopLon)
    lastPair = min(pairs, key=partial(dist, coord))

    # index of closest coordinate to stop
    # tells us last coordinate to load
    endLocationIndex = pairs.index(lastPair)

    print "TakeSpread:"
    locationGenerator = takespread(range(1, len(pairs)-1), 23)
    for i in locationGenerator:
        test = str(pairs[i][0]) + ", " + str(pairs[i][1])
        locations.append(test)

    # insert starting location location as first location element
    locations.append(str(stopLat) + ", " + str(stopLon))
    # insert user
    locations.insert(0, str(startLat) + ", " + str(startLon))
    # locations.insert(str(pairs[endLocationIndex][0]) + ", " + str(pairs[endLocationIndex][1]))

    print locations

    url = 'https://www.mapquestapi.com/directions/v2/route?json={"locations":["%s"]}&timeType=1&useTraffic=true\
    &outFormat=json&key=tAY5u0ki3CMdkv7GoGxT7ctvXEaKCSX9' % '", "'.join(map(str, locations))

    response = requests.get(url).json()
    return jsonify(response)

# choose num elements from sequence distributed as evenly as possible
def takespread(sequence, num):
    length = float(len(sequence))
    temp = []
    for i in range(num):
        yield sequence[int(ceil(i * length / num))]
