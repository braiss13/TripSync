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
    login = flask_login.login_manager.LoginManager()

    flapp.config.from_file("instance/config.json", json.load)
    login.init_app(flapp)
    flapp.register_blueprint(user_blpr)
    flapp.register_blueprint(trip_blpr)
    flapp.register_blueprint(score_blpr)
    return flapp, sirop, login
...


app, srp, lm = create_app()


@lm.unauthorized_handler
def unauthorized_handler():
    flask.flash("unauthorized")
    return flask.redirect("/")
...


@lm.user_loader
def user_loader(email: str) -> User:
    return User.find(srp, email)
...


@app.route("/favicon.ico")
def get_fav_icon():
    return app.send_static_file("favicon.ico")
...


@app.route("/login", methods=["POST"])
def login():
    if User.current():
        flask_login.logout_user()
        flask.flash("Ha pasado algo extraño. Por favor, entra de nuevo.")
        return flask.redirect("/")
    ...

    usr_email = flask.request.form.get("edEmail", "").strip()
    usr_pswd = flask.request.form.get("edPswd", "").strip()

    if (not usr_email
     or not usr_pswd):
        flask.flash("Credenciales incompletas")
        return flask.redirect("/")
    ...

    usr = User.find(srp, usr_email)

    if (not usr
     or not usr.chk_pswd(usr_pswd)):
        flask.flash("Credenciales incorrectas: ¿has hecho el registro?")
        return flask.redirect("/")
    ...

    flask_login.login_user(usr)
    return flask.redirect("/")
...


@flask_login.login_required
@app.route("/logout")
def logout():
    flask_login.logout_user()
    return flask.redirect("/")
...

# Arreglar
@app.route("/")
def main():
    usr = User.current()
    link_list = []

    if usr:
        link_list = srp.filter(Link, lambda l: l.usr_email == usr.email)
    ...

    sust = {
        "usr": usr,
        "srp": srp,
        "link_list": link_list
    }

    return flask.render_template("index.html", **sust)
...


if __name__ == "__main__":
    app.run(debug=True)
...
