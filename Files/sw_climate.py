import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """JSON list of stations from the dataset."""
    last_year_prcp = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').all()
           
    precipitation = []
    for date, prcp in last_year_prcp:
        precip_dict = {}
        precip_dict[date] = prcp
        #precip_dict["prcp"] = prcp
        precipitation.append(precip_dict)
        
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    """JSON list of stations from the dataset."""
    stations = session.query(Station.station, Station.name).distinct(Station.station).all()
    
    all_stations = list(np.ravel(stations))
    
    return jsonify(all_stations)
           
@app.route("/api/v1.0/tobs")
def tobs():
    """JSON list of temperature Observations (tobs) for the previous year."""
    last_year_tobs = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23').all()
           
    temp_observations = []
    for date, tobs in last_year_tobs:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        temp_observations.append(tobs_dict)
        
    return jsonify(temp_observations)
                      
@app.route("/api/v1.0/<start>")
def startdate(start = none):
    """JSON list of tmin, tmax, tavg for the dates greater than/equal to date entered"""
    # Query start date
    query_startdate = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    
    # Convert list of tuples into list
    list_startdate = list(query_startdate)

    # Jsonify the list
    return jsonify(list_startdate)
           
@app.route("/api/v1.0/<start>/<end>")
def daterange(start = None, end = None):
    """JSON list of tmin, tmax, tavg for the dates greater than/equal to date entered"""
    # Query
    query_rangedates = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()

    #Convert list of tuples into list
    list_rangedates = list(query_rangedates)
    
    # Jsonify the list
    return jsonify(list_rangedates)         

if __name__ == "__main__":
    app.run(debug=True)
