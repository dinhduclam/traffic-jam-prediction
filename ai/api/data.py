import numpy as np
from pydantic import BaseModel


class DataItem(BaseModel):
    timestamp: float
    X: float
    Y: float
    location: str
    velocity: float
    duration: float
    road_type: str
    road_condition: str
    road_event: str


class LiveDataItem:
    def __init__(self, timestamp: float, average_velocity: float,
                 average_duration: float,
                 road_type: str,
                 road_condition: str,
                 road_event: str):
        """
        :param timestamp:
        :param average_velocity:
        :param average_duration:
        :param road_type: int from 1 to 6 see constant file
        :param road_condition: int from 1 to 4 see constant file
        :param road_event: int from 1 to 7 see constant file
        """
        self.timestamp = timestamp
        self.average_velocity = average_velocity
        self.average_duration = average_duration
        self.road_type = road_type
        self.road_condition = road_condition
        self.road_event = road_event

    def get_input(self, encoder):
        road_type = encoder.transform([self.road_type])[0]
        _input = np.array([self.timestamp, self.average_velocity, self.average_duration, road_type])

        return _input.reshape(1, -1)


class HistoricalDataItem:
    def __init__(self, timestamp: float, X: float, Y: float, timeslot: int,
                 day_of_week: int,
                 day_of_month: int,
                 month_of_year: int):
        """
        :param timestamp: float
        :param X: longitude
        :param Y: latitude
        :param timeslot: int from 1 to 48
        :param day_of_week: int from 1 to 7
        :param day_of_month: int from 1 to 31
        :param month_of_year: int from 1 to 12
        """
        self.timestamp = timestamp
        self.X = X
        self.Y = Y
        self.timeslot = timeslot
        self.day_of_week = day_of_week
        self.day_of_month = day_of_month
        self.month_of_year = month_of_year

    def get_input(self, scaler):
        _input = np.array([self.timestamp, self.X, self.Y])

        return scaler.transform(_input.reshape(1, -1))
