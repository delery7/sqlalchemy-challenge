# Pull in packages

import numpy as np
import pandas as pd
import datetime as dt
import json
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement= Base.classes.measurement

# getting the latest date and one year back
latest_date=dt.date(2017,8,23)
delta=dt.timedelta(days=365)
one_year=latest_date-delta

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/><br/>"
        f"This api will get you all of the precipation data by date going back one year from the latest date in the data set:<br/>"
        f"/api/v1.0/precipitation<br/><br/>"
        f"This api will get you a list of the stations in the data set:<br/>"
        f"/api/v1.0/stations<br/><br/>"
        f"This api will get you the temperature data for the last year from the most active station in the data set:<br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"This api will get you the min, avg, and max temperature data going back to the entered start date:<br/>"
        f"Put in a date at the end of this string as Month-Day-Year.<br/> Example: http://127.0.0.1:5000//api/v1.0/startdate:/10-11-2016 <br/>"
        f"(Data returns in Min, Avg, Max order)<br/>"
        f"/api/v1.0/startdate:/<start><br/><br/>"
        f"This api will get you the min, avg, and max temperature data from the entered start date to the end date:<br/>"
        f"Put in a date after each date :/ as Month-Day-Year.<br/> Example: http://127.0.0.1:5000//api/v1.0/startdate:/10-11-2016/enddate:/12-10-2016<br/>"
        f"(Data returns in Min, Avg, Max order)<br/>"
        f"/api/v1.0/startdate:/<start>/enddate:/<end>"
    )

@app.route("/api/v1.0/precipitation")
def date_prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all dates and precipitation measurements
    results=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>one_year).all()
    session.close()

    # Convert list into normal list
    date_prcp = list(np.ravel(results))

    return jsonify(date_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for stations
    results=session.query(Station.name).filter(Measurement.station==Station.station).group_by(Measurement.station).all()
    session.close()
    # Convert list into normal list
    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def active():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for the active station data
    results=session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.date>one_year).\
        filter(Measurement.station=="USC00519281").all()
    session.close()

    # Convert list into normal list
    active = list(np.ravel(results))

    return jsonify(active)

@app.route("/api/v1.0/startdate:/<start>")
def startdate(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    start = dt.datetime.strptime(start, '%m-%d-%Y')
       
    # Query for data from the user defined start date

    inter=[func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    results=session.query(*inter).\
        filter(Measurement.date>=start).all()

    session.close()

    # Convert list of tuples into normal list
    startdate = list(np.ravel(results))

    return jsonify(startdate)


@app.route("/api/v1.0/startdate:/<start>/enddate:/<end>")
def startend(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    start = dt.datetime.strptime(start, '%m-%d-%Y')
    end = dt.datetime.strptime(end, '%m-%d-%Y')   
    
    # Query for data from the user defined start and end dates
    inter=[func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    results=session.query(*inter).\
        filter(Measurement.date>=start).filter(Measurement.date<=end).all()

    session.close()

    # Convert list of tuples into normal list
    startend = list(np.ravel(results))
    
    return jsonify(startend)

if __name__ == '__main__':
    app.run(debug=True)




