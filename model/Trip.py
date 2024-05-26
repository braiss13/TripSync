from datetime import datetime
from .User import User
from .Score import Score

class Trip:

    def __init__(self, time: datetime, origin: str, destination: str, duration: int, fare: int | float, creator: tuple[str, str]) -> None:
        self.__time: datetime = time
        self.__origin: str = origin
        self.__destination: str = destination
        self.__duration: int = duration
        self.__fare: float = fare
        self.__creator: tuple[str, str] = creator

        # List of participant and score IDs (id, name + surname):
        self.__participants: list[tuple[str, str]] = []
        self.__scores: list[tuple[str, str, str, str]] = []

    def get_id(self, srp) -> str:
        return srp.safe_from_oid(self.__oid__)

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
        if not isinstance(value, str):
            raise ValueError("Origin must be a string")

        self.__origin = value

    @property
    def destination(self):
        return self.__destination

    @destination.setter
    def destination(self, value):
        if not isinstance(value, str):
            raise ValueError("Destination must be a string")

        self.__destination = value

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, value):
        if not isinstance(value, int):
            raise ValueError("Duration must be an integer")

        self.__duration = value

    @property
    def fare(self):
        return self.__fare

    @fare.setter
    def fare(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Fare must be an integer or a float")

        self.__fare = float(value)

    # Participant-related logic:

    @property
    def participants(self):
        return self.__participants

    def add_participant(self, user: User) -> None:
        """Add a participant to the trip.

        Args:
            user (User): The user to add as a participant.
        """
        if user.get_id() not in [participant[0] for participant in self.__participants]:
            self.__participants.append((user.get_id(), user.name + " " + user.surname))

    def is_participant(self, user: User) -> bool:
        """Check whether a user is a participant of the trip.

        Args:
            user (User): The user to check.

        Returns:
            bool: True if the user is a participant, False otherwise.
        """
        return user.get_id() in [participant[0] for participant in self.__participants]

    # Score-related logic:

    @property
    def scores(self):
        return self.__scores

    def add_score(self, score_id: str, score: Score) -> None:
        """Add a score to the trip.
        
        This method stores scores as a tuple containing (in order):
        - The score ID.
        - The score creator's ID and full name (id, full_name).
        - The score rating.
        - The score comment.
        - The score date.

        Args:
            score (Score): The score to add.
        """
        if score_id not in [score[0] for score in self.__scores]:
            self.__scores.append((score_id, score.creator, score.rating, score.comment, score.date))

    def has_reviewed(self, user: User) -> bool:
        """Determine whether a user has reviewed the trip.
        
        Args:
            user (User): The user to check.
            
        Returns:
            bool: True if the user has reviewed the trip, False otherwise.
        """
        return user.get_id() in [score[1][0] for score in self.__scores]

    @property
    def creator(self) -> str:
        return self.__creator
