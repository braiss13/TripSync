import flask_login
import sirope
import werkzeug.security as safe

# This class defines the Users, with the attributes email, password, name, surname, age and phone
# with their respective getters and setters

class User(flask_login.mixins.UserMixin):

    def __init__(self, email: str, password: str, name: str, surname: str, age: int | str, phone: str) -> None:
        self.__email: str = email
        self.__pswd: str = safe.generate_password_hash(password)
        self.__name: str = name
        self.__surname: str = surname
        self.__age: int | str = age
        self.__phone: str = phone

    def get_id(self) -> str:
        return self.__email

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
    
    # Getters and setters:

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if not isinstance(value, str):
            raise TypeError("Email must be a string")

        self.__email = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        
        self.__name = value

    @property
    def surname(self):
        return self.__surname

    @surname.setter
    def surname(self, value):
        if not isinstance(value, str):
            raise TypeError("Surname must be a string")
        
        self.__surname = value

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        if not isinstance(value, int) and not isinstance(value, str):
            raise TypeError("Age must be an integer or a string")
        
        self.__age = value

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        if not isinstance(value, str):
            raise TypeError("Phone must be a string")
        
        self.__phone = value
