from enum import Enum

DEFAULT_TIME_OPEN = [(8, 16), (8, 16), (8, 16), (8, 16), (8, 16)]
WEEKDAYS = [
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),]


class TimespanActionEnum(Enum):
    SEND = 1
    RECEIVE = 2

