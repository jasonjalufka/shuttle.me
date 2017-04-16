import logging
from init import app
import views, api, alexa

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    logging.getLogger('flask_ask').setLevel(logging.DEBUG)
