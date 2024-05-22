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

    @property
    def origin(self):
        return self.__origin

    @property
    def destination(self):
        return self.__destination

    @property
    def duration(self):
        return self.__duration
    
    @property
    def user_id(self):
        return self.__user_id

    @property
    def fare(self):
        return self.__fare
    
    def get_safe_id(self, srp):
        return srp.safe_from_oid(self.__oid__)

    def get_formatted_time(self):
        dt = datetime.strptime(self.__time, '%Y-%m-%dT%H:%M')
        return dt.strftime('%d-%m-%Y %H:%M')