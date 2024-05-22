import sirope
from datetime import datetime


class Trip():
    def __init__(self, time, origin, destination, duration, fare, user_id):
        self.__time = time
        self.__origin = origin
        self.__destination = destination
        self.__duration = duration
        self.__fare = fare
        self.__user_id = user_id

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, value):
        self.__time = value

    @property
    def origin(self):
        return self.__origin

    @origin.setter
    def origin(self, value):
        self.__origin = value

    @property
    def destination(self):
        return self.__destination

    @destination.setter
    def destination(self, value):
        self.__destination = value

    @property
    def duration(self):
        return self.__duration
    
    @duration.setter
    def duration(self, value):
        self.__duration = value

    @property
    def user_id(self):
        return self.__user_id

    @property
    def fare(self):
        return self.__fare
    
    @fare.setter
    def fare(self, value):
        self.__fare = value

    def get_safe_id(self, srp):
        return srp.safe_from_oid(self.__oid__)

    def get_formatted_time(self):
        dt = datetime.strptime(self.__time, '%Y-%m-%dT%H:%M')
        return dt.strftime('%d-%m-%Y %H:%M')
