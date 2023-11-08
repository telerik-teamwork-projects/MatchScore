from enum import Enum


class Role(Enum):
    USER = "user"
    ADMIN = "admin"
    DIRECTOR = "director"

    def __str__(self):
        return str(self.value).capitalize()


class MatchFormat(Enum):
    TIME = "time"
    SCORE = "score"

    def __str__(self):
        return str(self.value).capitalize() + ' limited'
