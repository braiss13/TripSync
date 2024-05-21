import flask
import sirope
from flask_login import login_required, current_user
from model.Score import Score
from model.User import User
from model.Trip import Trip

def get_blprint():
    score_module = flask.blueprints.Blueprint("score_blpr", __name__,
                                              url_prefix="/score",
                                              template_folder="templates/score",
                                              static_folder="static")
    srp = sirope.Sirope()
    return score_module, srp

score_blpr, srp = get_blprint()

@score_blpr.route("/add", methods=["GET", "POST"])
@login_required
def score_add():
    if flask.request.method == "POST":
        trip_id = flask.request.form.get("edTripId", "").strip()
        user_id = flask.request.form.get("edUserId", "").strip()
        rating = flask.request.form.get("edRating", "").strip()

        if (not trip_id or not user_id or not rating):
            flask.flash("All fields are required.")
            return flask.redirect("/score/add")

        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError
        except ValueError:
            flask.flash("Rating must be an integer between 1 and 5.")
            return flask.redirect("/score/add")

        trip = srp.find_first(Trip, lambda t: t.get_safe_id(srp) == trip_id)
        user = srp.find_first(User, lambda u: u.get_safe_id(srp) == user_id)

        if not trip or not user:
            flask.flash("Invalid Trip ID or User ID.")
            return flask.redirect("/score/add")

        score = Score(trip_id, user_id, rating)
        srp.save(score)
        flask.flash("Score added successfully.")
        return flask.redirect("/")
    
    return flask.render_template("score/add_score.html")

@score_blpr.route("/list", methods=["GET"])
@login_required
def score_list():
    scores = srp.filter(Score, lambda s: s.user_id == current_user.id)
    return flask.render_template("score/list_scores.html", scores=scores)
