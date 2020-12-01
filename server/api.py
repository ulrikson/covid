import requests
from datetime import date, timedelta, datetime
from sqlalchemy import create_engine, text
import psycopg2
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def dbConnect():
    # uri = "postgresql+psycopg2://postgres:kebabpizza@localhost:5432/covid" #LOCAL
    uri = "postgres+psycopg2://odcvsrneqygagr:faa8ba613866ce9b68fda849c5752268684b07c77cdbcc4924386c70b8a993af@ec2-52-208-138-246.eu-west-1.compute.amazonaws.com:5432/df3b0t7h21j3io"

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


def lastDbDate():
    conn = dbConnect()

    query = text("""
        SELECT MAX(report_date) FROM sweden
    """)

    result = conn.execute(query).fetchone()

    if result[0] == None:
        firstCovidCase = '2020-02-25'
        result = [datetime.strptime(firstCovidCase, '%Y-%m-%d').date()]

    conn.dispose()

    return result[0]


def updateDb():

    # creating timedelta for fetching data
    start = lastDbDate()
    end = date.today()

    # if updated today or yesterday (api has a 1 day delay)
    if start >= end-timedelta(days=1):
        return None

    # db connect and data fetch
    conn = dbConnect()
    data = fetch(start+timedelta(days=1), end)

    # Looping and comparing to the day before
    for index,day in enumerate(data):
        current = data[index]
        last = data[index-1]

        # setting the diffs to previous days, replacing negative values with 0
        confirmedDiff = current["Confirmed"]-last["Confirmed"]
        deathsDiff = current["Deaths"]-last["Deaths"]
        daysDiff = {
            'confirmed_diff': confirmedDiff if confirmedDiff >= 0 else 0,
            'deaths_diff': deathsDiff if deathsDiff >= 0 else 0,
        }

        if index > 0 or len(data) == 1:
            query = text(f"""
                INSERT INTO sweden (report_date, confirmed, confirmed_diff, deaths, deaths_diff)
                VALUES ('{current["Date"]}', '{current["Confirmed"]}', '{daysDiff['confirmed_diff']}', '{current["Deaths"]}', '{daysDiff['deaths_diff']}')
            """)
        else:
            query = text(f"""
                INSERT INTO sweden (report_date, confirmed, confirmed_diff, deaths, deaths_diff)
                VALUES ('{current["Date"]}', '{current["Confirmed"]}', '{current["Confirmed"]}', '{current["Deaths"]}', '{current["Deaths"]}' )
            """)

        conn.execute(query)
        # print(query) # for debugging
    
    conn.dispose()

    return 'success'


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


def simpleLinear(settings):

    data = timeline(settings)

    x = np.array(data['labels']).reshape((-1,1))
    y = np.array(data['covid_data'])

    # y = bo + b1x + b2x^2 + b3x^3
    polynom = PolynomialFeatures(degree=4, include_bias=False).fit_transform(x)

    model = LinearRegression().fit(polynom, y)


    r_square = model.score(polynom,y)
    predictions = model.predict(polynom).tolist()

    # ! utilize later
    # lastDataLabel = data['labels'][-1]
    # x_future = np.arange(lastDataLabel+1, lastDataLabel+60).reshape(-1,1)
    # futurePredictions = model.predict(x_future)

    json = {
        'labels': data['labels'],
        'covid_data': data['covid_data'],
        'predict': predictions,
        'r_square': r_square
    }

    return json


# settings = {
#     'period': 'doy',
#     'statistica': 'deaths_diff'
# }

# test = simpleLinear(settings)
# print(test['r_square'])