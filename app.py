import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

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
    return (
        f"List all available api routes:<br/>"
        f" <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

#------------------------------------------------   
@app.route('/api/v1.0/precipitation')
def precipitation():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    percipitation_data = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["Date"] = date
        precipitation_dict["Precipitation"] = prcp
        precipitation_data.append(precipitation_dict)

    return jsonify(perciptation_data)

#------------------------------------------------   
@app.route('/api/v1.0/stations')
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query list of stations data
    results = session.query(Station.station, Station.name).all()

    session.close()

    station_list = []
    for station, name in results
    station_dict = {}
    station_dict["Station ID"] = station
    station_dict["Station Name"] = name

    station_data.append(station_dict)
    
    return jsonify(station_data)