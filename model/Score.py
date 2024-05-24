import sirope
from datetime import datetime

class Score:
    def __init__(self, trip, user, rating, comment="", date=None):
        self.__trip = trip
        self.__user = user
        self.__rating = rating
        self.__comment = comment
        self.__date = date if date else datetime.now()

    @property
    def trip(self):
        return self.__trip

    @property
    def user(self):
        return self.__user

    @property
    def rating(self):
        return self.__rating

    @property
    def comment(self):
        return self.__comment

    @property
    def date(self):
        return self.__date
    
    def get_safe_id(self, srp):
        return srp.safe_from_oid(self.__oid__)

    def to_dict(self):
        return {
            "trip": self.__trip.to_dict(),
            "user": self.__user.to_dict(),
            "rating": self.__rating,
            "comment": self.__comment,
            "date": self.__date.strftime('%Y-%m-%d %H:%M:%S')
        }
