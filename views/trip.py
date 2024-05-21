import flask
import sirope
from flask_login import login_required, current_user
from model.Trip import Trip
from model.User import User
from datetime import datetime

def get_blprint():
    trip_module = flask.blueprints.Blueprint("trip_blpr", __name__,
                                             url_prefix="/trip",
                                             template_folder="templates/trip",
                                             static_folder="static")
    srp = sirope.Sirope()
    return trip_module, srp

trip_blpr, srp = get_blprint()

@trip_blpr.route("/add", methods=["GET", "POST"])
@login_required
def trip_add():
    if flask.request.method == "POST":
        time = flask.request.form.get("edTime", "").strip()
        origin = flask.request.form.get("edOrigin", "").strip()
        destination = flask.request.form.get("edDestination", "").strip()
        duration = flask.request.form.get("edDuration", "").strip()
        fare = flask.request.form.get("edFare", "").strip()

        if not time or not origin or not destination or not duration or not fare:
            flask.flash("All fields are required.", "danger")
            return flask.redirect("/trip/add")
        try:
            duration = int(duration)
            fare = float(fare)
        except ValueError:
            flask.flash("Duration must be an integer and fare must be a number.", "danger")
            return flask.redirect("/trip/add")

        trip = Trip(time, origin, destination, duration, fare, current_user.get_id())
        srp.save(trip)
        flask.flash("Trip added successfully.", "success")
        return flask.redirect("/")
    
    usr = current_user
    min_date_time = datetime.now().strftime('%Y-%m-%dT%H:%M')
    return flask.render_template("trip/add_trip.html", usr=usr, min_date_time=min_date_time)

@trip_blpr.route("/list", methods=["GET"])
@login_required
def trip_list():
    trips = srp.filter(Trip, lambda t: t.user_id == current_user.get_id())
    return flask.render_template("trip/list_trips.html", trips=trips)
