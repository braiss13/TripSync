import sirope
from datetime import datetime
from .User import User
from .Score import Score

class Trip:
    def __init__(self, time: datetime, origin: str, destination: str, duration: int, fare: int | float, creator: dict) -> None:
        self.__time: datetime = time
        self.__origin: str = origin
        self.__destination: str = destination
        self.__duration: int = duration
        self.__fare: float = float(fare)
        self.__creator: dict = creator
        
        # Instance-generated attributes:
        self.__participants: list[dict] = []
        self.__scores: list[dict] = []

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
    def fare(self):
        return self.__fare
    
    @fare.setter
    def fare(self, value):
        self.__fare = value
    
    @property
    def participants(self):
        return self.__participants

    def add_participant(self, participant_email):
        if participant_email not in self.__participants:
            self.__participants.append(participant_email)

    def is_participant(self, user):
        return user.id in [participant['id'] for participant in self.__participants]
    
    @property
    def scores(self):
        return self.__scores
    
    @property
    def creator(self):
        return self.__creator
    
    def add_score(self, user, score):
        if not user.id in [score['user']['id'] for score in self.scores]:
            self.scores.append(score)
    
    def can_add_score(self, user):
        return not user.id in [score['user']['id'] for score in self.scores]
    
    def get_safe_id(self, srp):
        return srp.safe_from_oid(self.__oid__)

    def get_formatted_time(self):
        dt = datetime.strptime(self.__time, '%Y-%m-%dT%H:%M')
        return dt.strftime('%d-%m-%Y %H:%M')
    """
    def to_dict(self):
        return {
            "time": self.__time,
            "origin": self.__origin,
            "destination": self.__destination,
            "duration": self.__duration,
            "fare": self.__fare,
            "creator": self.__creator.to_dict(),
            "participants": self.__participants,
            "scores": self.__scores
        }
    """