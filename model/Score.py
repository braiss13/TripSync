from datetime import datetime

# This class defines the Score, with the attributes rating, comment, creator (score_creator) and date 
# with their respective getters and setters

class Score:

    def __init__(self, rating: int, comment: str, creator: tuple[str, str]):
        self.__rating: int = int(rating)
        self.__comment: str = comment
        self.__creator: tuple[str, str] = creator
        
        self.__date: datetime = datetime.now()

    def get_id(self, srp) -> str:
        return srp.safe_from_oid(self.__oid__)

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, value):
        if not isinstance(value, str):
            raise ValueError("User must be a string")
        
        self.__user = value

    @property
    def rating(self):
        return int(self.__rating)

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int):
            raise ValueError("Rating must be an integer")
        
        if not 0 <= value <= 5:
            raise ValueError("Rating must be between 0 and 5")

        self.__rating = int(value)

    @property
    def comment(self):
        return self.__comment

    @comment.setter
    def comment(self, value):
        self.__comment = value

    @property
    def creator(self):
        return self.__creator

    @property
    def date(self):
        return self.__date
