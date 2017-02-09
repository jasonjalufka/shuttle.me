from flask import Flask
from doublemap import DoubleMap


app = Flask(__name__)


tracker = DoubleMap('txstate')

@app.route('/')
def hello_world():
    return tracker


if __name__ == '__main__':
    app.run()
