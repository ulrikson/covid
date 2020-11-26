import requests
from datetime import date, timedelta, datetime
from sqlalchemy import create_engine, text
import psycopg2


def dbConnect():
    uri = "postgresql+psycopg2://postgres:kebabpizza@localhost:5432/covid"
    conn = create_engine(uri)
    return conn


def fetch(dateFrom, dateTo):
    params = {
        'dateFrom': dateFrom,
        'dateTo': dateTo,
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
    yesterday = date.today() - timedelta(days=1)
    end =  yesterday

    # if already updated today
    if start == end:
        return 'already updated'

    # db connect
    conn = dbConnect()

    data = fetch(start, end)

    # Looping and comparing to the day before
    for index,day in enumerate(data):
        current = data[index]
        last = data[index-1]

        if index > 0:
            query = text(f"""
                INSERT INTO sweden (report_date, confirmed, confirmed_diff, deaths, deaths_diff)
                VALUES ('{current["Date"]}', '{current["Confirmed"]}', '{current["Confirmed"]-last["Confirmed"]}', '{current["Deaths"]}', '{current["Deaths"]-last["Deaths"]}')
            """)
        else:
            query = text(f"""
                INSERT INTO sweden (report_date, confirmed, confirmed_diff, deaths, deaths_diff)
                VALUES ('{current["Date"]}', '{current["Confirmed"]}', '{current["Confirmed"]}', '{current["Deaths"]}', '{current["Deaths"]}' )
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
    covid_data = [data[1] for data in result]

    # converting to dict
    json = {
        'labels': labels,
        'covid_data': covid_data
    }

    return json
