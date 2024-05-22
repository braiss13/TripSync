import flask
import flask_login
import sirope
from model.User import User
from model.Trip import Trip

def get_blprint():
    usr_module = flask.blueprints.Blueprint("user_blpr", __name__,
                                            url_prefix="/user",
                                            template_folder="templates/user",
                                            static_folder="static")
    syrp = sirope.Sirope()
    return usr_module, syrp

user_blpr, srp = get_blprint()

@user_blpr.route("/add", methods=["POST"])
def user_add():
    usr_email = flask.request.form.get("edEmail", "").strip()
    usr_passw = flask.request.form.get("edPswd", "").strip()
    usr_name = flask.request.form.get("edName", "").strip()
    usr_surname = flask.request.form.get("edSurname", "").strip()
    usr_age = flask.request.form.get("edAge", "").strip()
    usr_phone = flask.request.form.get("edPhone", "").strip()

    if not usr_email or not usr_passw or not usr_name or not usr_surname or not usr_age or not usr_phone:
        flask.flash("All fields are required.", "danger")
        return flask.redirect("/")

    if User.find(srp, usr_email):
        flask.flash("User already exists.", "danger")
        return flask.redirect("/")

    usr = User(usr_email, usr_passw, usr_name, usr_surname, int(usr_age), usr_phone)
    srp.save(usr)
    flask_login.login_user(usr)
    flask.flash("Registration successful! You are now logged in.", "success")

    # Obtener la lista de viajes para el usuario recién registrado
    trip_list = list(srp.filter(Trip, lambda t: t.user_id == usr.email))
    
    sust = {
        "usr": usr,
        "srp": srp,
        "trip_list": trip_list
    }

    return flask.render_template("index.html", **sust)

@user_blpr.route("/profile/<user_id>")
def user_profile(user_id):
    usr = srp.find_first(User, lambda u: u.email == user_id)

    if not usr:
        flask.flash("User not found.", "danger")
        return flask.redirect("/")

    return flask.render_template("user_profile.html", user=usr)