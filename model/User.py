from __future__ import annotations

import flask_login
import sirope
import werkzeug.security as safe

def generate_uuid(email: str) -> str:
    """Generate a unique user identifier based on the email address.
    
    The process is described as follows:
        1. Get the ASCII code of each letter in the email address (ord).
        2. Convert the ASCII code to a string and fill it with zeros to make it 3 characters long (zfill).
        3. Concatenate all the strings obtained in the previous step.
    
    Args:
        email: The email address of the user.
        
    Returns:
        A unique identifier for the user.
    """
    return "".join(f"{str(ord(letter)).zfill(3)}" for letter in email)

class User(flask_login.mixins.UserMixin):
    def __init__(self, email: str, password: str, name: str, surname: str, age: int | str, phone: str) -> None:
        self.__email: str = email
        self.__pswd: str = safe.generate_password_hash(password)
        self.__name: str = name
        self.__surname: str = surname
        self.__age: int | str = age
        self.__phone: str = phone
        
        self.id = generate_uuid(self.email)

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
    def find(srp: sirope.Sirope, email: str) -> User:
        return srp.find_first(User, lambda u: u.email == email)

    def get_full_name(self):
        return f"{self.__name} {self.__surname}"

    
    def to_dict(self):
        return {
            "email": self.__email,
            "name": self.__name,
            "surname": self.__surname,
            "age": self.__age,
            "phone": self.__phone,
            "id": self.id
        }
    
    def __repr__(self):
        return f"User({self.__email}, {self.__name}, {self.__surname}, {self.__age}, {self.__phone})"
    
    def __str__(self):
        return f"User({self.__email}, {self.__name}, {self.__surname}, {self.__age}, {self.__phone})"
        