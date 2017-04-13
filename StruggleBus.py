import logging
from init import app
import views, api, alexa

if __name__ == '__main__':
    app.run(debug=True)
    logging.getLogger('flask_ask').setLevel(logging.DEBUG)
