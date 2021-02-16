import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)


@app.route("/")
def home_page():
    """List of available api routes:"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"        
    )


# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23').all()
    prcp_dict = dict(prcp_results)
    print("Precipitation Results")
    return jsonify(prcp_dict) 


# Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    station_list = session.query(Station.station).order_by(Station.station).all() 
    print("Station List:")   
    for row in station_list:
        print (row[0])
    return jsonify(station_list)


# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.


@app.route('/api/v1.0/tobs/')
def tobs():
    tobs_results = session.query(Measurement.tobs).order_by(Measurement.date).all()
    print("Temperature Results for All Stations")
    return jsonify(tobs_results)


# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>")
def combined_start_stats(start):
    q = session.query(Station.id,
                  Station.station,
                  func.min(Measurement.tobs),
                  func.max(Measurement.tobs),
                  func.avg(Measurement.tobs))\
                  .filter(Measurement.station == Station.station)\
                  .filter(Measurement.date >= start).all()                  
    print("Min, Max and Avg Temps with start date: ({start})")
    for row in q:
        print()
        print(row)
    return jsonify(q)

@app.route("/api/v1.0/<start>/<end>")
def combined_start_end_stats(start,end):
    q = session.query(Station.id,
                  Station.station,
                  func.min(Measurement.tobs),
                  func.max(Measurement.tobs),
                  func.avg(Measurement.tobs))\
                  .filter(Measurement.station == Station.station)\
                  .filter(Measurement.date <= end)\
                  .filter(Measurement.date >= start).all()
    print(f"Min, Max and Avg Temps with start date: ({start}) and date ({end})")
    for row in q:
        print()
        print(row)
    return jsonify(q)



if __name__ == '__main__':
    app.run(debug=True)
