import flask
import sirope
from flask_login import login_required, current_user

from model.Score import Score

def get_blprint():
    score_module = flask.blueprints.Blueprint("score_blpr", __name__,
                                              url_prefix="/score",
                                              template_folder="templates/score",
                                              static_folder="static")
    srp = sirope.Sirope()
    return score_module, srp

score_blpr, srp = get_blprint()

@score_blpr.route("/add/<trip_id>", methods=["GET", "POST"])
@login_required
def score_add(trip_id):
    if flask.request.method == "POST":
        rating = flask.request.form.get("edRating", "").strip()
        comment = flask.request.form.get("edComment", "").strip()

        trip = srp.load(srp.oid_from_safe(trip_id))
        
        if not rating:
            flask.flash("Rating is required.", "danger")
            return flask.redirect(f"/score/add/{trip_id}")
        
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError
        except ValueError:
            flask.flash("Rating must be an integer between 1 and 5.", "danger")
            return flask.redirect(f"/score/add/{trip_id}")
        
        score = Score(trip_id, current_user.email, rating, comment)
        srp.save(score)
        trip.add_score(score.get_safe_id(srp))
        srp.save(trip)
        flask.flash("Rating added successfully.", "success")
        return flask.redirect("/")
    
    return flask.render_template("add_score.html", usr=current_user, trip_id=trip_id)
