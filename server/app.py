from flask import Flask, render_template, request
from server.api import timeline, movingAverage, multipleLinearRegression, latestStats, arima
from server.newsparser import getNewsPosts
from dotenv import load_dotenv
import os
load_dotenv()

# Set up the app and point it to Vue
app = Flask(__name__, static_folder='../client/dist/',    static_url_path='/')

@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/timeline', methods=['POST'])
def getTimeline():
    settings = request.get_json()
    return timeline(settings)


@app.route('/latest-stats', methods=['GET'])
def getLatest():
    return latestStats()


@app.route('/moving', methods=['POST'])
def getMoving():
    settings = request.get_json()
    return movingAverage(settings)


@app.route('/linear', methods=['POST'])
def getLinear():
    settings = request.get_json()
    return multipleLinearRegression(settings)


@app.route('/arima', methods=['POST'])
def getArima():
    settings = request.get_json()
    return arima(settings)


@app.route('/news', methods=['GET'])
def getNews():
    return getNewsPosts()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)