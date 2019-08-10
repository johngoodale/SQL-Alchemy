import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool
# For the SQLite engine connection: https://stackoverflow.com/questions/33055039/using-sqlalchemy-scoped-session-in-theading-thread

from flask import Flask, jsonify

#################################################

# Database Setup

#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite" connect_args={"check same thread": False}, poolclass=StaticPool, echo=True)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create session link from python to database
session = Session(engine)

#################################################

# Flask Setup

#################################################

app = Flask(__name__)

#################################################

# Flask Routes

#################################################
# Home
@app.route("/")
def welcome():
	"""List all API routes"""
	return """<html>
<h1>Hawaii Weather API</h1>
<img src="http://blue-hawaii.com/wp-content/uploads/2015/07/3.jpg" alt="Hawaii"/>
<p>Precipitation:</p>
<ul>
  <li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></li>
</ul>
<p>Stations:</p>
<ul>
  <li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>
</ul>
<p>Temperature:</p>
<ul>
  <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>
</ul>
<p>Start Date:</p>
<ul>
  <li><a href="/api/v1.0/2017-07-28">/api/v1.0/2017-07-28</a></li>
</ul>
<p>Start & End Date:</p>
<ul>
  <li><a href="/api/v1.0/2017-07-28/2017-08-04">/api/v1.0/2017-07-28/2017-08-04</a></li>
</ul>
</html>
"""


# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
        # Convert the Query Results to a Dictionary Using `date` as the Key and `prcp` as the Value
        # Calculate the Date 1 Year Ago from the Last Data Point in the Database
		start_dp = dt.date(2017,8,23) - dt.timedelta(days=365)
		# Design a query to retrieve the last 12 months of precipitation data and plot the results
		precip = session.query(Measurement.date, Measurement.prcp).\
		filter(Measurement.date >= start_dp).\
		order_by(Measurement.date).all()
        # Convert List of Tuples Into a Dictionary
        precip_list = dict(precip)
        # Return JSON Representation of Dictionary
        return jsonify(precip_list)

# Station Route
@app.route("/api/v1.0/stations")
def stations():
        # Return a JSON List of Stations
        all_stations = session.query(Station.station, Station.name).all()
        # Convert List of Tuples Into Normal List
        station_list = list(all_stations)
        # Return JSON List of Stations from the Dataset
        return jsonify(station_list)

# TOBs Route
@app.route("/api/v1.0/tobs")
def tobs():
        # Query for the Dates and Temperature Observations from a Year from the Last Data Point
        start_dp = dt.date(2017,8,23) - dt.timedelta(days=365)
        # Design a query to retrieve the last 12 months of precipitation data and plot the results
        most_tobs = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= start_dp).\
                order_by(Measurement.date).all()
        # Convert List of Tuples Into Normal List
        tobs_list = list(most_tobs)
        # Return JSON List of Temperature Observations (tobs) for the Previous Year
        return jsonify(tobs_list)

# Start Day Route
@app.route("/api/v1.0/<start>")
def start_day(start):
        start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()
        # Convert List of Tuples Into Normal List
        start_day_list = list(start_day)
        # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start Range
        return jsonify(start_day_list)

# Start-End Day Route
@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
        start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()
        # Convert List of Tuples Into Normal List
        start_end_day_list = list(start_end_day)
        # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start-End Range
        return jsonify(start_end_day_list)

# Define Main Behavior
if __name__ == '__main__':
    app.run(debug=True)
