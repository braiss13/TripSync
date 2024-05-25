import json
import flask
import flask_login
import sirope

from model.User import User
from model.Trip import Trip
from model.Score import Score

from views.user import user_blpr
from views.trip import trip_blpr
from views.score import score_blpr

def create_app():
    flapp = flask.Flask(__name__)
    sirop = sirope.Sirope()
    login = flask_login.LoginManager()

    flapp.config.from_file("instance/config.json", json.load)
    login.init_app(flapp)
    flapp.register_blueprint(user_blpr)
    flapp.register_blueprint(trip_blpr)
    flapp.register_blueprint(score_blpr)
    return flapp, sirop, login

app, srp, lm = create_app()

@lm.unauthorized_handler
def unauthorized_handler():
    flask.flash("Unauthorized access", "danger")
    return flask.redirect("/")

@lm.user_loader
def user_loader(email: str) -> User:
    return User.find(srp, email)

@app.route("/favicon.ico")
def get_fav_icon():
    return app.send_static_file("favicon.ico")

@app.route("/login", methods=["POST"])
def login():
    if User.current():
        flask_login.logout_user()
        flask.flash("Something strange happened. Please log in again.", "danger")
        return flask.redirect("/")
    
    usr_email = flask.request.form.get("edEmail", "").strip()
    usr_pswd = flask.request.form.get("edPswd", "").strip()

    if not usr_email or not usr_pswd:
        flask.flash("Incomplete credentials", "danger")
        return flask.redirect("/")
    
    usr = User.find(srp, usr_email)

    if not usr or not usr.chk_pswd(usr_pswd):
        flask.flash("Incorrect credentials: Have you registered?", "danger")
        return flask.redirect("/")
    
    flask_login.login_user(usr)
    flask.flash("Login successful!", "success")
    return flask.redirect("/")

@flask_login.login_required
@app.route("/logout")
def logout():
    flask_login.logout_user()
    flask.flash("You have been logged out.", "success")
    return flask.redirect("/")

@app.route("/")
def main():
    usr = User.current()
    my_trip_list = []
    other_trip_list = []

    if usr:
        my_trip_list = [(trip.to_dict(), f"{usr.name} {usr.surname}") for trip in srp.filter(Trip, lambda t: t.user_id == usr.email)]
        
        for trip in srp.filter(Trip, lambda t: t.user_id != usr.email):
            creator = User.find(srp, trip.user_id)
            creator_name = f"{creator.name} {creator.surname}"
            participants = [f"{User.find(srp, p).name} {User.find(srp, p).surname}" for p in trip.participants]

            score_list = srp.load_all(Score)    
            
            trip_dict = trip.to_dict()
            trip_dict['safe_id'] = trip.get_safe_id(srp)

            other_trip_list.append((trip.to_dict(), creator_name, participants, score_list))

    sust = {
        "usr": usr,
        "srp": srp,
        "my_trip_list": my_trip_list,
        "other_trip_list": other_trip_list
    }

    return flask.render_template("index.html", **sust)


if __name__ == "__main__":
    app.run(debug=True)
