"""Модуль с константами."""
from enum import Enum


class Status(Enum):
    """Класс статусов task."""
    NO_STATUS = 'no_status'
    WORKING_ON = 'working_on'
    FINISHED = 'finished'
