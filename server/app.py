from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from api import timeline, updateDb

# instantiate the app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/timeline', methods=['GET'])
@cross_origin()
def getTimeline():
    return timeline()


@app.route('/refresh', methods=['GET'])
def getFreshData():
    return updateDb()


if __name__ == '__main__':
    app.run(debug=True)