import flask_login
import sirope
import werkzeug.security as safe

class User(flask_login.mixins.UserMixin):
    def __init__(self, email, pswd, name, surname, age, phone):
        self.__email = email
        self.__pswd = safe.generate_password_hash(pswd)
        self.__name = name
        self.__surname = surname
        self.__age = age
        self.__phone = phone

    @property
    def email(self):
        return self.__email

    @property
    def name(self):
        return self.__name

    @property
    def surname(self):
        return self.__surname

    @property
    def age(self):
        return self.__age

    @property
    def phone(self):
        return self.__phone

    def get_id(self):
        return self.email

    def chk_pswd(self, other_pswd):
        return safe.check_password_hash(self.__pswd, other_pswd)

    @staticmethod
    def current():
        usr = flask_login.current_user

        if usr.is_anonymous:
            flask_login.logout_user()
            usr = None

        return usr

    @staticmethod
    def find(srp: sirope.Sirope, email: str) -> "User":
        return srp.find_first(User, lambda u: u.email == email)
    
    def to_dict(self):
        return {
            "email": self.__email,
            "name": self.__name,
            "surname": self.__surname,
            "age": self.__age,
            "phone": self.__phone
        }
