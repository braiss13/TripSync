import flask
import sirope
from model.User import User

def get_blprint():
    usr_module = flask.blueprints.Blueprint("user_blpr", __name__,
                                            url_prefix="/user",
                                            template_folder="templates",
                                            static_folder="static")
    srp = sirope.Sirope()
    return usr_module, srp

user_blpr, srp = get_blprint()

@user_blpr.route("/add", methods=["POST"])
def user_add():
    usr_email = flask.request.form.get("edEmail", "").strip()
    usr_passw = flask.request.form.get("edPswd", "").strip()

    if not usr_email or not usr_passw:
        flask.flash("Missing credentials...", "danger")
        return flask.redirect("/")
    
    if User.find(srp, usr_email):
        flask.flash("User already exists!", "danger")
        return flask.redirect("/")
    
    usr = User(usr_email, usr_passw)
    srp.save(usr)
    flask.flash("You can now log in with your new credentials.", "success")
    return flask.redirect("/")
