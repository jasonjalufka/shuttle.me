from flask import Flask
import flask
from doublemap import DoubleMap


app = Flask(__name__)

display = []

tracker = DoubleMap('txstate')
# print(tracker.stop_info(1))
# dictionary so when passed 71, it is trying to match id
# var = input("Select your route ")
# print("you selected", var)

# for routekey, routevalue in tracker.routes.iteritems():
#     for value in routevalue["stops"]:
#         if value is var:
#             print "Your stop is on the %s route (%d)" %(routevalue["name"], routekey)
#             print routevalue
#             display = routevalue["path"]
#             print display
#

for stopkey, stopvalue in tracker.stops.iteritems():
    print stopvalue["name"]
    display.append(stopvalue["name"])


#print(tracker.routes[397]["path"])
#print(tracker.buses[427]["route"])
#print(tracker.routes[tracker.buses[427]["route"]])

# render map location takes in 2 arg, displays map


@app.route('/')
def hello_world():
    print display
    return flask.render_template("index.html", data=display)
   # return flask.render_template("index.html", tracker.routes[tracker.buses[427]["route"]["u'color"]])


if __name__ == '__main__':
    app.run()
