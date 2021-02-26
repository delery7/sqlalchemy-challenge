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

start=('2016-08-01')
session = Session(engine)
start = dt.datetime.strptime(start, '%Y-%m-%d')
# end = dt.datetime.strptime(start, '%Y-%m-%d')   
# Query for start date
results=session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date>start).all()
# print(results)
session.close()
# Convert list of tuples into normal list
startdate = list(np.ravel(results))
print(startdate)

# results=session.query(Measurement.station, Measurement.date, Measurement.tobs).\
#     filter(Measurement.date>one_year).\
#     filter(Measurement.station=="USC00519281").all()
# session.close()
# # Convert list of tuples into normal list
# active = list(np.ravel(results))

# print(active)