from enum import Enum


class BaseEnum(Enum):

    def choices(self):
        return [(x.name, x.value) for x in self]


class GenderEnum(BaseEnum):
    MALE = "male"
    FEMALE = "female"


class RoleEnum(BaseEnum):
    ADMIN = "admin"
    USER = "user"
