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

@score_blpr.route("/add/<trip_id>", methods=["GET", "POST"])
@login_required
def score_add(trip_id):
    if flask.request.method == "POST":
        rating = flask.request.form.get("edRating", "").strip()
        comment = flask.request.form.get("edComment", "").strip()
        
        trip = srp.load(srp.oid_from_safe(trip_id))
        user = current_user  # revisar

        try:
            rating = int(rating)
        except Exception:
            rating = 0
            
        score = Score(user.to_dict(), rating, comment)
        srp.save(score)
        trip.add_score(user, score.to_dict()) 
        srp.save(trip)
        flask.flash("Rating added successfully.", "success")
        return flask.redirect("/")
    
    return flask.render_template("add_score.html", usr=current_user, trip_id=trip_id)
