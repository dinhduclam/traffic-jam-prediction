from datetime import datetime

from fastapi import FastAPI

from data import DataItem, LiveDataItem, HistoricalDataItem

# create instance of fastapi
app = FastAPI()


def estimate(item: DataItem):
    # process request
    live_data = LiveDataItem(item.velocity, item.duration, item.road_type, item.road_condition, item.road_event)
    timeslot, day_of_week, day_of_month, month_of_year = convert_timestamp(item.timestamp)
    historical_data = HistoricalDataItem(timeslot, day_of_week, day_of_month, month_of_year)
    # call the pretrained model and predict
    result = 0
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
