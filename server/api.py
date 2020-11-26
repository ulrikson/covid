import requests
from datetime import date, timedelta, datetime
from sqlalchemy import create_engine, text
import psycopg2


def dbConnect():
    uri = "postgresql+psycopg2://postgres:kebabpizza@localhost:5432/covid"
    conn = create_engine(uri)
    return conn


def fetch(date):
    params = {
        'date': date,
        'iso': 'SWE'
    }

    response = requests.get('https://covid-api.com/api/reports', params=params)
    data = response.json()
    return data


def aggregate(data):
    
    # create new dict with value for date (first results date)
    aggregated = {
        'confirmed': 0,
        'deaths': 0,
        'recovered': 0,
        'active': 0,
        'confirmed_diff': 0,
        'deaths_diff': 0,
        'recovered_diff': 0,
        'active_diff': 0
    }

    # for loop and add to the values
    for key in aggregated:
        for region in data['data']:
            aggregated[key] += region[key]

    # return new dict with aggregated data
    return aggregated


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
    yesterday = date.today() - timedelta(days=1)
    end =  yesterday
    delta = end - start

    # if already updated today
    if start == end:
        return 'already updated'

    # db connect
    conn = dbConnect()

    # looping dates in timedelta, fetching that days data from API and inserting into DB
    for i in range(delta.days + 1):
        day = start + timedelta(days=i)
        
        data = fetch(day)
        aggregated = aggregate(data)

        query = text(f"""
            INSERT INTO sweden (report_date, confirmed, deaths, recovered, active, confirmed_diff, deaths_diff, recovered_diff, active_diff)
            VALUES ('{day}', '{aggregated["confirmed"]}', '{aggregated["deaths"]}', '{aggregated["recovered"]}', '{aggregated["active"]}', '{aggregated["confirmed_diff"]}', '{aggregated["deaths_diff"]}', '{aggregated["recovered_diff"]}', '{aggregated["active_diff"]}')
        """)

        conn.execute(query)
    
    conn.dispose()

    return 'success'


def timeline(scope):
    # sql query to fetch all data points
    conn = dbConnect()

    query = text(f"""
     SELECT report_date, confirmed_diff FROM sweden
     WHERE report_date > '{scope['startDate']}'
    """)

    result = conn.execute(query).fetchall()

    conn.dispose()

    # convert into 2 array (to start with), date (label) and confirmed (data)
    labels = [data[0].strftime("%Y-%m-%d") for data in result]
    confirmed_diff = [data[1] for data in result]

    # converting to dict
    json = {
        'labels': labels,
        'confirmed_diff': confirmed_diff
    }

    return json
