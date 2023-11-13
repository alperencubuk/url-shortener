from enum import Enum


class Sort(str, Enum):
    ID = "id"
    TIMES_CLICKED = "times_clicked"


class Order(str, Enum):
    ASC = "asc"
    DESC = "desc"
