import requests
from datetime import date, timedelta, datetime
from sqlalchemy import create_engine, text
import psycopg2
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

import os
from dotenv import load_dotenv
load_dotenv()

def dbConnect():
    # uri = "postgresql+psycopg2://postgres:kebabpizza@localhost:5432/covid" #LOCAL
    uri = os.getenv("HEROKU_URI")

    conn = create_engine(uri)
    return conn


def fetch(dateFrom, dateTo):
    params = {
        'from': dateFrom,
        'to': dateTo,
    }

    response = requests.get('https://api.covid19api.com/country/sweden', params=params)
    data = response.json()
    return data


def timeline(settings):
    # sql query to fetch all data points
    conn = dbConnect()

    query = text(f"""
        SELECT
            DATE_PART('{settings['period']}', report_date) AS SCOPE,
            DATE_PART('year', report_date) AS YEAR,
            SUM({settings['statistica']}) AS {settings['statistica']}
        FROM sweden
        group by YEAR, SCOPE
        order by YEAR, SCOPE
    """)

    result = conn.execute(query).fetchall()

    conn.dispose()

    # convert into 2 array (to start with), date (label) and confirmed (data)
    labels = [data[0] for data in result]
    covidData = [data[2] for data in result]

    # converting to dict
    json = {
        'labels': labels,
        'covid_data': covidData
    }

    return json


def movingAverage(settings):
    data = timeline(settings)

    df = pd.DataFrame(data)

    df['rolling'] = df['covid_data'].rolling(settings['window'], min_periods=1).mean() #! replace with parameter

    json = {
        'labels': data['labels'],
        'covid_data': df['rolling'].to_list()
    }

    return json


def multipleLinearRegression(settings):

    data = timeline(settings)

    # setting up data
    x = np.array(data['labels']).reshape((-1,1))
    y = np.array(data['covid_data'])

    # Fitting data    
    polynom = PolynomialFeatures(degree=3, include_bias=False).fit_transform(x) # y = bo + b1x + b2x^2 + b3x^3
    model = LinearRegression().fit(polynom, y)
    r_square = model.score(polynom,y)

    # Generating future predictions
    firstDataLabel = data['labels'][0]
    startOfPrediction = data['labels'][-1] + 1
    endOfPrediction = startOfPrediction+30
    predictData= [*range(int(firstDataLabel), int(endOfPrediction), 1)]

    x_predict = np.array(predictData).reshape((-1,1))
    predictPolynom = PolynomialFeatures(degree=3, include_bias=False).fit_transform(x_predict)
    predictions = model.predict(predictPolynom).tolist()

    rationalPredictions = [0 if nr < 0 else nr for nr in predictions] #rational as confirmed/deaths cannot be negative

    json = {
        'labels': predictData,
        'covid_data': data['covid_data'],
        'predict': rationalPredictions,
        'r_square': r_square
    }

    return json


def latestStats():
    conn = dbConnect()

    query =text("""
        SELECT report_date, confirmed, deaths FROM sweden
        ORDER BY report_date DESC
        LIMIT 1
    """)

    result = conn.execute(query).fetchone()
    conn.dispose()

    json = {
        'report_date': result[0],
        'confirmed': result[1],
        'deaths': result[2]
    }

    return json


mockSettings = {
    'period': 'doy',
    'statistica': 'confirmed_diff'
}