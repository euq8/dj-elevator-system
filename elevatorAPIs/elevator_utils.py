from enum import Enum


class AbstractEnum(Enum):
    @classmethod
    def choices(cls):
        return [
            (enum_item.value, enum_item.value) 
            for enum_item in cls.__members__.values()
        ]


class State(AbstractEnum):
    MOVING = "moving"
    STOPPED = "stopped"
    IDLE = "idle"
    MAINTENANCE = "maintenance"


class Direction(AbstractEnum):
    UP = "up"
    DOWN = "down"


class RequestType(AbstractEnum):
    EXT = "external"
    INT = "internal"
