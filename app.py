import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect = True)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind = engine)

# Find the most recent date in the data set.
session.query(Measurement.date).order_by(Measurement.date.desc()).first()

# Design a query to retrieve the last 12 months of precipitation data and plot the results. 
# Starting from the most recent data point in the database. 

# Calculate the date one year from the last date in data set.
dates = dt.date(2017,8,23)-dt.timedelta(days = 365)

# Perform a query to retrieve the data and precipitation scores
precipitation_scores = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= "2016-08-23").\
    order_by(Measurement.date).all()
precipitation_scores

# Save the query results as a Pandas DataFrame and set the index to the date column
precip_df = pd.DataFrame(precipitation_scores, columns=['Date', 'Precipitation'])
precip_df.set_index('Date', inplace=True)

# Sort the dataframe by date
precip_df = precip_df.sort_values(by='Date', ascending=True)


from flask import flask, jsonify

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def Home_page():
    """List all available api routes."""
    return (
        f"Available Routes:<br>"
        f"==================================================<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/&lt;date&gt; (replace &lt;date&gt; with date in yyyy-mm-dd format)<br>"
        f"/api/v1.0/&lt;date&gt;/&lt;date&gt; (replace &lt;date&gt;/&lt;date&gt; with date in yyyy-mm-dd/yyyy-mm-dd format)<br>"
    )

# /api/v1.0/precipitation
# convert the query results to a dictionary using date as the key and prep as the value
# return the JSON representation

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(bind = engine)
    # Query all prcp
    dates = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    dates # datetime.date(2016, 8, 23)
    # Perform a query to retrieve the data and precipitation scores
    precipitation_scores = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= (2016, 8, 23).\
            order_by(Measurement.date).all()
    
    
@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset.
    session = Session(bind = engine)
    #     """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all stations
    session.query(Station.station, Station.name).all()
    session.close()
#     Station_list = list(results) #list(np.ravel(results))
    Station_list = []
    for stat in results:
        d = {
        "Station":stat[0],
        "Station Name":stat[1]
        }
        Station_list.append(d)
    
    return jsonify(Station_list)

@app.route("/api/v1.0/tobs")
# Return a JSON list of temperature observations (TOBS) for the previous year
def tobs():
    session = Session(engine)
    dates = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    dates # datetime.date(2016, 8, 23)
    # Query all stations
    precipitation_scores = session.query(Measurement.date, Measurement.tobs)\
                .filter(Measurement.station == 'USC00519281', Measurement.date.between(dates, dt.date(2017, 8, 23)))\
                .group_by(Measurement.date)\
                .order_by(Measurement.date)
    session.close()

    tobs_list = []
    for tob in results:
        d={
        "Date":tob[0],
        "Temperature":tob[1]
        }
        tobs_list.append(d)
    return jsonify(tobs_list)



if __name__ == '__main__':
    app.run(debug=True)