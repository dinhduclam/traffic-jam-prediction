from datetime import datetime

import joblib
import numpy as np
from fastapi import FastAPI
from keras.models import load_model

from data import DataItem, LiveDataItem, HistoricalDataItem

# create instance of fastapi
app = FastAPI()

hbdpe_scaler = joblib.load('.././scaler/hbdpe_minmax_model.pkl')
lbdpe_encoder = joblib.load('.././encoder/ldbpe_encoder_model.pkl')
hdbpe_model = load_model('.././trained-model/best_historical_cost_model.model')
ldbpe_model = load_model('.././trained-model/best_live_model.model')


def estimate(item: DataItem):
    # process request
    ldbpe_input = LiveDataItem(timestamp=item.timestamp, average_velocity=item.velocity, average_duration=item.duration,
                               road_type=item.road_type, road_condition=item.road_condition, road_event=item.road_event)
    timeslot, day_of_week, day_of_month, month_of_year = convert_timestamp(item.timestamp)
    hbdpe_input = HistoricalDataItem(timestamp=item.timestamp, X=item.X, Y=item.Y, timeslot=timeslot,
                                     day_of_week=day_of_week, day_of_month=day_of_month, month_of_year=month_of_year)
    # call the pretrained model and predict

    hbdpe_pred = hdbpe_model.predict(hbdpe_input.get_input(hbdpe_scaler))
    p1 = hbdpe_pred.max()
    print("p1 = ", p1)

    lbdpe_pred = ldbpe_model.predict(np.array([ldbpe_input.get_input(encoder=lbdpe_encoder)]))
    p2 = lbdpe_pred.max()
    print("p2 = ", p2)
    result = (p1 * p2) / ((p1 * p2) + (1 - p1) * (1 - p2))
    print("result = ", result)
    result = 0 if result < 0.5 else 1
    return result


def convert_timestamp(timestamp: int | float):
    dt_object = datetime.fromtimestamp(timestamp)
    # convert to time
    time = dt_object.time()

    # Calculate the number of minutes since midnight (00:00)
    minutes_since_midnight = time.hour * 60 + time.minute

    # Divide the minutes since midnight by the length of each timeslot (30 minutes)
    timeslot = minutes_since_midnight // 30

    # Get day of week (Monday = 0, Sunday = 6)
    day_of_week = dt_object.weekday()
    day_of_week += 1
    day_of_month = dt_object.day
    month_of_year = dt_object.month
    return timeslot, day_of_week, day_of_month, month_of_year


@app.post("/predict")
def predict(item: DataItem):
    result = estimate(item)
    return result
