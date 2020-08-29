import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt
from datetime import datetime, date, time, timedelta

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available api routes."""
    return(
        f"List all available api routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>tobs</a><br/>"
        f"<a href='/api/v1.0/<start>'>start</a><br/>"
        f"<a href='/api/v1.0/<start>/<end>'>start/finish</a>"
    )

#------------------------------------------------   
@app.route('/api/v1.0/precipitation')
def precipitation():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    precipitation_data = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["Date"] = date
        precipitation_dict["Precipitation"] = prcp
        precipitation_data.append(precipitation_dict)

    return jsonify(precipitation_data)

#------------------------------------------------   
@app.route('/api/v1.0/stations')
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query list of stations data
    results = session.query(Station.station, Station.name).all()

    session.close()

    station_list = []
    for station, name in results:
        station_dict = {}
        station_dict["Station ID"] = station
        station_dict["Station Name"] = name

        station_list.append(station_dict)
    
    return jsonify(station_list)

#------------------------------------------------   
@app.route('/api/v1.0/tobs')
def tobs():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query list of temperature observation data

    # Calculate the date 1 year ago from last date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Query the most frequent station for all tobs from the last year
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= prev_year).all()

    session.close()

    # Unravel results into a 1D array and convert to a list
    temperatures = list(np.ravel(results))

    return jsonify(temperatures)

#------------------------------------------------   
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        # calculate TMIN, TAVG, TMAX for dates greater than start
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        # Unravel results into a 1D array and convert to a list
        temps = list(np.ravel(results))
        return jsonify(temps)
    # calculate TMIN, TAVG, TMAX with start and stop
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
    
if __name__ == '__main__':
    app.run(debug=True)