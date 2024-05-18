# Contenido generado por ChatGPT, ¡¡REVISAR!!

from flask import Blueprint, render_template, request, redirect, url_for
from model.Trip import Trip
import sirope

trip_bp = Blueprint('trips', __name__)

@trip_bp.route('/trips')
def index():
    s = sirope.Sirope()
    trips = list(s.load_all(Trip))
    return render_template('index.html', trips=trips)

@trip_bp.route('/trips/add', methods=['GET', 'POST'])
def add_trip():
    if request.method == 'POST':
        time = request.form['time']
        origin = request.form['origin']
        destination = request.form['destination']
        duration = request.form['duration']
        fare = request.form['fare']

        new_trip = Trip(time, origin, destination, duration, fare)
        s = sirope.Sirope()
        s.save(new_trip)

        return redirect(url_for('trips.index'))
    
    return render_template('add_trip.html')
