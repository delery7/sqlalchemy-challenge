import numpy as np
import pandas as pd
import datetime as dt

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
engine = create_engine("sqlite:///hawaii.sqlite")

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/startdate:/<start><br/>"
        f"/api/v1.0/startdate:/<start>/enddate:/<end>"
    )

@app.route("/api/v1.0/precipitation")
def date_prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all dates and precipitation measurements
    results=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>one_year).all()
    session.close()

    # Convert list of tuples into normal list
    date_prcp = list(np.ravel(results))

    return jsonify(date_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for stations
    results=session.query(Station.name).filter(Measurement.station==Station.station).group_by(Measurement.station).all()
    session.close()
    # Convert list of tuples into normal list
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
    # Convert list of tuples into normal list
    active = list(np.ravel(results))

    return jsonify(active)

# @app.route("/api/v1.0/startdate:/<start>")
# def startdate(start):
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     # Query all passengers
#     results=session.query(Measurement.station, Measurement.date, Measurement.tobs).\
#         filter(Measurement.date>one_year).\
#         filter(Measurement.station=="USC00519281").all()
#     session.close()
#     # Convert list of tuples into normal list
#     startdate = list(np.ravel(results))

#     return jsonify(active)

# @app.route("/api/v1.0/startdate:/<start>/enddate:/<end>")
# def active():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     # Query all passengers
#     results=session.query(Measurement.station, Measurement.date, Measurement.tobs).\
#         filter(Measurement.date>one_year).\
#         filter(Measurement.station=="USC00519281").all()
#     session.close()
#     # Convert list of tuples into normal list
#     active = list(np.ravel(results))

#     return jsonify(active)

if __name__ == '__main__':
    app.run(debug=True)




