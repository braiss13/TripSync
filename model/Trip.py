import sirope

class Trip(sirope.Model):
    def init(self, time, origin, destination, duration, fare):
        self.__time = time
        self.__origin = origin
        self.__destination = destination
        self.__duration = duration
        self.__fare = fare

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
