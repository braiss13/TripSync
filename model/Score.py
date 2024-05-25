import sirope
from datetime import datetime
from .User import User

class Score:
    
    def __init__(self, user: dict, rating: int = 0, comment: str = "", date: datetime | None = None):
        self.__user: dict = user
        self.__rating: int = int(rating)
        self.__comment: str = comment
        self.__date: datetime = date if date is not None else datetime.now()

    @property
    def user(self):
        return self.__user

    @property
    def rating(self):
        return int(self.__rating)

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
            "user": self.__user,
            "rating": int(self.__rating),
            "comment": self.__comment,
            "date": self.__date.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def __repr__(self) -> str:
        return f"Score({self.__user}, {self.__rating}, {self.__comment}, {self.__date})"
    
    def __str__(self) -> str:
        return f"Score({self.__user}, {self.__rating}, {self.__comment}, {self.__date})"