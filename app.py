import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Access the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite",connect_args={'check_same_thread': False})
#reflect the data base into a new model
Base = automap_base()
Base.prepare(engine, reflect= True)

# With the database reflected save the references to variables for each table.
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database
session = Session(engine)

# Create Flask application called app
# To understand: Notice the __name__ variable in this code. This is a special type of variable in Python.
# Its value depends on where and how the code is run.
# For example, if I wanted to import the app.py file into another Python file named example.py, the variable __name__ would be set to example
app = Flask(__name__)
# The __name__ variable will be set to __main__. This indicates that we are not using any other file to run this code.

# Define the Welcome route
@app.route('/')
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!<br>
    Available Routes:<br>
    /api/v1.0/precipitation<br>
    /api/v1.0/stations<br>
    /api/v1.0/tobs<br>
    /api/v1.0/temp/start/end<br>
    ''')

# Create Precipitation route
@app.route('/api/v1.0/precipitation')
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip) 

#Create Stations Route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


if __name__ == "__main__":
    app.run(debug=True)
