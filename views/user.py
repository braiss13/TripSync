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
    email = flask.request.form.get("edEmail", "").strip()
    password = flask.request.form.get("edPswd", "").strip()
    name = flask.request.form.get("edName", "").strip()
    surname = flask.request.form.get("edSurname", "").strip()
    age = flask.request.form.get("edAge", "").strip()
    phone = flask.request.form.get("edPhone", "").strip()

    if not (email or password or name or surname or age or phone):
        flask.flash("All fields are required.", "danger")
        return flask.redirect("/")

    if User.find(srp, email):
        flask.flash("User already exists.", "danger")
        return flask.redirect("/")

    usr = User(email, password, name, surname, age, phone)
    srp.save(usr)
    flask_login.login_user(usr)
    flask.flash("Registration successful! You are now logged in.", "success")

    return flask.redirect("/")

@user_blpr.route("/profile/<user_id>")
def user_profile(user_id):
    usr = srp.find_first(User, lambda user: user.get_id() == user_id)

    if not usr:
        flask.flash("User not found.", "danger")
        return flask.redirect("/")

    return flask.render_template("user_profile.html", user=usr)