import sirope
from datetime import datetime


class Score():
    def __init__(self, trip_id, user_id, rating, comment="", date=None):
        self.__trip_id = trip_id
        self.__user_id = user_id
        self.__rating = rating
        self.__comment = comment
        self.__date = date if date else datetime.now()

    @property
    def trip_id(self):
        return self.__trip_id

    @property
    def user_id(self):
        return self.__user_id

    @property
    def rating(self):
        return self.__rating

    @property
    def comment(self):
        return self.__comment

    @property
    def date(self):
        return self.__date
