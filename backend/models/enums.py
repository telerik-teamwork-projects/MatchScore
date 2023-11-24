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

    def __str__(self):
        return str(self.value).capitalize()


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


class KnockoutRounds(Enum):
    EIGHTH_FINALS = (1, "Eighth-finals")
    QUARTERFINALS = (2, "Quarterfinals")
    SEMIFINALS = (3, "Semifinals")
    FINAL = (4, "Final")
    THIRD_PLACE = (5, "3th Place Match")

    @classmethod
    def from_int(cls, i: int):
        for r in cls:
            if r.value[0] == i:
                return r.value[1]
        raise ValueError(cls.__name__ + f' has no value matching round {i}')
