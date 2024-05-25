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
    # Map class constructor arguments to form fields:
    names = {
        "email": "edEmail",
        "password": "edPswd",
        "name": "edName",
        "surname": "edSurname",
        "age": "edAge",
        "phone": "edPhone"
    }
    
    # Get form fields and strip them:
    fields = {
        key: flask.request.form.get(value, "").strip()
        for key, value in names.items()
    }
    
    # Ensure all fields are filled:
    if not all(fields.values()):
        flask.flash("All fields are required.", "danger")
        return flask.redirect("/")
    
    # Check if user already exists:
    if User.find(srp, fields["email"]):
        flask.flash("User already exists.", "danger")
        return flask.redirect("/")

    usr = User(**fields)
    srp.save(usr)
    flask_login.login_user(usr)
    flask.flash("Registration successful! You are now logged in.", "success")

    return flask.redirect("/")

@user_blpr.route("/profile/<user_id>")
def user_profile(user_id):
    usr = srp.find_first(User, lambda user: user.id == user_id)

    if not usr:
        flask.flash("User not found.", "danger")
        return flask.redirect("/")

    return flask.render_template("user_profile.html", user=usr)