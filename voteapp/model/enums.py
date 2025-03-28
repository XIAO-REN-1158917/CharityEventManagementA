from enum import Enum


class Role(Enum):
    VOTER = "voter"
    SCRUTINEER = "scrutineer"
    ADMIN = "admin"


class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class CompetitionStatus(Enum):
    PENDING = "pending"
    ONGOING = "ongoing"
    ENDED = "ended"
    PUBLISHED = "published"


class VoteStatus(Enum):
    VALID = "valid"
    INVALID = "invalid"
