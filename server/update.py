from datetime import date, timedelta, datetime
from api import latestStats, dbConnect, fetch
from sqlalchemy import create_engine, text
import psycopg2

def updateDb():

    # creating timedelta for fetching data
    latest = latestStats()
    start = latest['report_date']
    end = date.today()

    # if updated today or yesterday (api has a 1 day delay)
    if start >= end-timedelta(days=1):
        return 'already updated'

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

        # if more > 1 date to be updated, takes diff to last instance
        if index > 0:
            query = text(f"""
                INSERT INTO sweden (report_date, confirmed, confirmed_diff, deaths, deaths_diff)
                VALUES ('{current["Date"]}', '{current["Confirmed"]}', '{daysDiff['confirmed_diff']}', '{current["Deaths"]}', '{daysDiff['deaths_diff']}')
            """)
        # if only 1 to be updated, takes diff to last db value
        else:
            query = text(f"""
                INSERT INTO sweden (report_date, confirmed, confirmed_diff, deaths, deaths_diff)
                VALUES ('{current["Date"]}', '{current["Confirmed"]}', '{current["Confirmed"]-latest['confirmed']}', '{current["Deaths"]}', '{current["Deaths"]-latest["deaths"]}' )
            """)

        conn.execute(query)
    
    conn.dispose()

    return 'success'

updateDb()