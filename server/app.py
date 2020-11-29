from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from api import timeline, updateDb, movingAverage, simpleLinear

# instantiate the app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/timeline', methods=['POST'])
@cross_origin()
def getTimeline():
    settings = request.get_json()
    return timeline(settings)


@app.route('/moving', methods=['POST'])
@cross_origin()
def getMoving():
    settings = request.get_json()
    return movingAverage(settings)


@app.route('/linear', methods=['POST'])
@cross_origin()
def getLinear():
    settings = request.get_json()
    return simpleLinear(settings)


@app.route('/refresh', methods=['GET'])
def getFreshData():
    return updateDb()


if __name__ == '__main__':
    app.run(debug=True)