from enum import Enum


class Role(Enum):
    USER = "user"
    ADMIN = "admin"
    DIRECTOR = "director"

    def __str__(self):
        return str(self.value).capitalize()


class TournamentStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"

class TournamentFormat(Enum):
    KNOCKOUT = "knockout"
    LEAGUE = "league"

class MatchFormat(Enum):
    TIME = "time"
    SCORE = "score"

    def __str__(self):
        return str(self.value).capitalize() + ' limited'


class TournamentFormat(Enum):
    KNOCKOUT = "knockout"
    LEAGUE = "league"

    def __str__(self):
        return str(self.value).capitalize()


class Request(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"