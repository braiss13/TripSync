import sirope
from datetime import datetime

class Score(sirope.Model):
    def __init__(self, trip_id, user_id, rating, date=None):
        self.__trip_id = trip_id
        self.__user_id = user_id
        self.__rating = rating
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
    def date(self):
        return self.__date
