import requests
import datetime
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
    }

    # for loop and add to the values
    for key in aggregated:
        for region in data['data']:
            aggregated[key] += region[key]

    # return new dict with aggregated data
    return aggregated


def getFromDB():
    conn = dbConnect()

    query = text("""
        SELECT * FROM sweden
    """)
    
    result = conn.execute(query).fetchone()

    print(result)


def main():
    data = fetch('2020-11-20')
    aggregated = aggregate(data)
    getFromDB()

main()