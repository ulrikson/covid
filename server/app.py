from flask import Flask, render_template, request
from server.api import timeline, updateDb, movingAverage, simpleLinear
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


@app.route('/moving', methods=['POST'])
def getMoving():
    settings = request.get_json()
    return movingAverage(settings)


@app.route('/linear', methods=['POST'])
def getLinear():
    settings = request.get_json()
    return simpleLinear(settings)


@app.route('/refresh', methods=['GET'])
def getFreshData():
    return updateDb()