import copy
import datetime

import requests


class DoubleMap(object):
    """
    DoubleMap bus route tracker.
    Params: string organization (example: 'iupui')
    """
    def __init__(self, organization):
        self.__domain = 'http://txstate.doublemap.com/map/v2'

    def bus_info(self, bus_id):
        """ Get information about a specific bus id. """
        return self.buses[bus_id]

    def route_info(self, route_id):
        """ Get information about a specific route id. """
        return self.routes[route_id]

    def stop_info(self, stop_id):
        """ Get information about a specific stop id. """
        return self.stops[stop_id]

    def get_route(tracker, stop_id):
        """ Find the user's route """
        possible_routes = set()
        for route_id, route in tracker.routes.iteritems():
            if stop_id in route['stops']:
                return route_id


    def eta(self, stop_id, route_id):
        """ Get eta (in minutes) about a specific stop id and route_id. """
        etas_url = self.__domain + "/eta?stop=" + str(stop_id)
        # their api is hacky here
        etas = requests.get(etas_url).json()['etas'][str(stop_id)]['etas']
        for eta in etas:
            if eta['route'] == int(route_id):
                return eta['avg']
        else:
            # if there is no eta information available
            return -1

    @property
    def buses(self):
        """ Returns a dict of buses indexed by id. """
        buses = {}
        bus_url = self.__domain + "/buses"
        buses_response = requests.get(bus_url).json()
        # add each bus to the dict of buses
        for bus in buses_response:
            bus_info = copy.deepcopy(bus)
            bus_info.pop('id', None)
            # check if the latitude and longitude are valid
            if bus_info['lat'] != -1 and bus_info['lon'] != -1:
                buses[bus['id']] = bus_info

        return buses

    @property
    def routes(self):
        """ Returns a dict of routes indexed by id. """
        routes = {}
        routes_url = self.__domain + "/routes"
        routes_response = requests.get(routes_url).json()
        # add each route to the dict of routes
        for route in routes_response:
            route_info = copy.deepcopy(route)
            route_info.pop('id', None)
            routes[route['id']] = route_info

        return routes

    @property
    def stops(self):
        """ Returns a dict of stops indexed by id. """
        stops = {}
        stops_url = self.__domain + "/stops"
        stops_response = requests.get(stops_url).json()
        # add each stop to the dict of stops
        for stop in stops_response:
            stop_info = copy.deepcopy(stop)
            stop_info.pop('id', None)
            stops[stop['id']] = stop_info

        return stops


def main():
    print("printing from main")
    # Fix for Python 2.x.
    try:
        input = raw_input
    except NameError:
        pass
    print("Enter the DoubleMap route area (ex: iupui):")
    tracker = DoubleMap(input('>> '))

    print("Choose a starting point:")
    start = select_location(tracker)

    print("Choose a destination:")
    finish = select_location(tracker)

    route = find_route(tracker, start, finish)
    bus_name = tracker.routes[route]['name']

    if route != -1:
        bus_arrive_time = tracker.eta(start, route)
        print("The %s bus will arrive in %s minute(s)." % \
                (bus_name, bus_arrive_time))
    else:
        print("A single route cannot be taken.")


def select_location(tracker):
    """ Prompt the user for a location and return the stop_id. """
    try:
        input = raw_input
    except NameError:
        pass
    for stop_id, stop in tracker.stops.iteritems():
        print("%s. %s" % (stop_id, stop['name']))

    return int(input('>> '))


def find_route(tracker, start, finish):
    """ Find which route the user should take. """
    possible_routes = set()
    for route_id, route in tracker.routes.iteritems():
        if start in route['stops']:
            possible_routes.add(route_id)
        if finish in route['stops']:
            possible_routes.add(route_id)

    for route_id in list(possible_routes):
        if start in tracker.routes[route_id]['stops'] and \
                finish in tracker.routes[route_id]['stops']:
            return route_id
    else:
        return -1


if __name__ == '__main__':
    main()
