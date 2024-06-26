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

        # Pass user as (id, full_name) tuple
        trip = Trip(time, origin, destination, duration, fare, (current_user.get_id(), current_user.name + " " + current_user.surname))
        srp.save(trip)
        flask.flash("Trip added successfully.", "success")
        return flask.redirect("/")

    usr = current_user
    min_date_time = datetime.now().strftime('%Y-%m-%dT%H:%M')
    return flask.render_template("add_trip.html", usr=usr, min_date_time=min_date_time, srp=srp)

@trip_blpr.route("/edit/<trip_id>", methods=["GET", "POST"])
@login_required
def trip_edit(trip_id):
    trip_oid = srp.oid_from_safe(trip_id)
    trip = srp.load(trip_oid)

    if flask.request.method == "POST":
        time = flask.request.form.get("edTime", "").strip()
        origin = flask.request.form.get("edOrigin", "").strip()
        destination = flask.request.form.get("edDestination", "").strip()
        duration = flask.request.form.get("edDuration", "").strip()
        fare = flask.request.form.get("edFare", "").strip()

        if not time or not origin or not destination or not duration or not fare:
            flask.flash("All fields are required.", "danger")
            return flask.redirect(f"/trip/edit/{trip_id}")
        try:
            duration = int(duration)
            fare = float(fare)
        except ValueError:
            flask.flash("Duration must be an integer and fare must be a number.", "danger")
            return flask.redirect(f"/trip/edit/{trip_id}")

        trip.time = time
        trip.origin = origin
        trip.destination = destination
        trip.duration = duration
        trip.fare = fare
        srp.save(trip)
        flask.flash("Trip updated successfully.", "success")
        return flask.redirect("/")

    usr = current_user
    min_date_time = datetime.now().strftime('%Y-%m-%dT%H:%M')
    return flask.render_template("edit_trip.html", trip=trip, usr=usr, min_date_time=min_date_time, srp=srp)

@login_required
@trip_blpr.route('/delete', methods=['POST'])
def trip_delete():
    trip_safe_id = flask.request.form.get("trip_id")
    trip_oid = srp.oid_from_safe(trip_safe_id)

    if not trip_oid:
        flask.flash("Invalid Trip ID.", "danger")
        return flask.redirect("/")

    if srp.exists(trip_oid):
        srp.delete(trip_oid)
        flask.flash("Trip deleted successfully.", "success")
    else:
        flask.flash("Trip not found.", "danger")

    return flask.redirect("/")


@login_required
@trip_blpr.route("/join", methods=["POST"])
def trip_join():
    trip_safe_id = flask.request.form.get("trip_id")

    if not trip_safe_id:
        flask.flash("Trip ID is missing.", "danger")
        return flask.redirect("/")

    trip_oid = srp.oid_from_safe(trip_safe_id)

    if not trip_oid:
        flask.flash("Invalid Trip ID.", "danger")
        return flask.redirect("/")

    trip = srp.load(trip_oid)
    usr = current_user

    if usr.get_id() not in [participant[0] for participant in trip.participants] and len(trip.participants) < 4:
        trip.add_participant(usr)
        srp.save(trip)
        flask.flash("You have successfully joined the trip.", "success")
    else:
        flask.flash("Unable to join the trip. Either you are already a participant or the trip is full.", "danger")

    return flask.redirect("/")