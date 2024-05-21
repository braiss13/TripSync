import sirope

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
    def fare(self):
        return self.__fare
    @property
    def get_id(self):
        return self.id