import json
import csv
import datetime

net_file = './data/net.json'
vehicle_file = './data/vehicle.json'

# Define class lane
class lane:
    def __init__(self, _id, _type, _speed, _length, _shape):
        self.id = _id
        self.type = _type
        self.speed = _speed
        self.length = _length
        self.shape = _shape

    def display(self):
        print(f"ID: {self.id}, Type: {self.type}, Speed: {self.speed}, Length: {self.length}, Shape: {self.shape}")

lanes = []

# Load data from json file and create vehicle array
with open(net_file) as json_file:
    data = json.load(json_file)
    
    edge = data['net']['edge']
    junction = data['net']['junction']
    connection = data['net']['connection']

    for i in edge:
        try:
            type_of_lane = i['type']
            if(type(i['lane']) == list):
                for j in i['lane']:
                    lanes.append(lane(j['id'], type_of_lane, j['speed'], j['length'], j['shape']))
            elif(type(i['lane']) == dict):
                j = i['lane']                    
                lanes.append(lane(j['id'], type_of_lane, j['speed'], j['length'], j['shape']))

        except KeyError:
            if(type(i['lane']) == list):
                for j in i['lane']:
                    lanes.append(lane(j['id'], 'highway.normal', j['speed'], j['length'], j['shape']))
            elif(type(i['lane']) == dict):
                j = i['lane']                    
                lanes.append(lane(j['id'], 'highway.normal', j['speed'], j['length'], j['shape']))
            print("Not have key type")

# Define class vehicle
class vehicle:
    def __init__(self, _time, _id, _x, _y, _angle, _speed, _pos, _lane, _duration, _condition, _event, _day_of_week, _day, _month, _year, _hour, _minute):
        self.time = _time
        self.id = _id
        self.x = _x
        self.y = _y
        self.angle = _angle
        self.speed = _speed
        self.pos = _pos
        self.lane = _lane
        self.duration = _duration
        self.condition = _condition
        self.event = _event
        self.day_of_week = int(_day_of_week)
        self.day = int(_day)
        self.month = int(_month)
        self.year = int(_year)
        self.hour = int(_hour)
        self.minute = int(_minute)

    def display(self):
        print(f"Time: {self.time}, id: {self.id}, X: {self.x}, Y: {self.y}, Angle: {self.angle}, Speed: {self.speed}, Position: {self.pos}, Lane: {self.lane}, Duration: {self.duration}, Condition: {self.condition}")

vehicles = []

with open(vehicle_file) as json_file:
    data = json.load(json_file)

    timestep = data['fcd-export']['timestep']

    for i in timestep:
        if (type(i['vehicle']) == list):
            for j in i['vehicle']:
                vehicles.append(vehicle(i['time'], j['id'], j['x'], j['y'], 
                       j['angle'], j['speed'], j['pos'], 
                       j['lane'], 0.0, "None", "None", 1, 1, 1, 2023, 0, 0))
        elif (type(i['vehicle']) == dict):
            vehicles.append(vehicle(i['time'], i['vehicle']['id'], i['vehicle']['x'], i['vehicle']['y'], 
                       i['vehicle']['angle'], i['vehicle']['speed'], i['vehicle']['pos'], 
                       i['vehicle']['lane'], 0.0, "None", "None", 1, 1, 1, 2023, 0, 0))

    new_vehicles = []

    # Classify data
    check = []
    for i in range(0, len(vehicles)):
        check.append(False)

    for i in range(0, len(vehicles)):
        temps = []
        if (check[i] == False):
            temps.append(vehicles[i])
            check[i] = True

            for j in range(i+1, len(vehicles)):
                if(vehicles[i].id == vehicles[j].id and check[j] == False):
                    temps.append(vehicles[j])
                    check[j] = True

            new_vehicles.append(temps)

    # Calculate duration and set congestion event
    current_day = 1

    for v in new_vehicles:
        duration = 0
        for i in range(1, len(v)):
            if v[i].pos == v[i-1].pos:
                duration += 0.1
                v[i].duration = duration
                if duration > 5:
                    v[i].event = "congestion"

        for i in range(0, len(v)):
            seconds = float(v[i].time)
            start_date = datetime.datetime(2023, 1, 1, 17, 0, 0)
            time_delta = datetime.timedelta(seconds=seconds)
            end_date = start_date + time_delta

            day = end_date.day
            month = end_date.month
            year = end_date.year
            hour = end_date.hour
            minute = end_date.minute
            second = end_date.second
            millisecond = end_date.microsecond // 1000
            current_date = datetime.datetime.now()
            day_of_week = end_date.strftime("%A")

            v[i].day_of_week = day_of_week
            v[i].day = day
            v[i].month = month
            v[i].year = year
            v[i].hour = hour
            v[i].minute = minute
            print(v[i].time, v[i].id, v[i].day_of_week, v[i].day, v[i].month, v[i].year)


class export: 
    def __init__(self, _id, _timestamp, _X, _Y, _velocity, _duration, _road_type, _road_condition, _road_event, _hour, _minute , _day_of_week, _day, _month, _year):
        self.id = _id
        self.timestamp = _timestamp
        self.latitudes = _X
        self.longtitudes = _Y
        self.velocity = _velocity
        self.duration = _duration
        self.road_type = _road_type
        self.road_condition = _road_condition
        self.road_event = _road_event
        self.day_of_week = _day_of_week
        self.day = _day
        self.month = _month
        self.year = _year
        self.hour = int(_hour)
        self.minute = int(_minute)

    def display(self):
        print(f"ID: {self.id} Timestamp: {self.timestamp}, Longtitudes: {self.longtitudes}, Latitudes: {self.latitudes}, velocity: {self.velocity}, duration: {self.duration}, road type: {self.road_type}, road condition: {self.road_condition}, road event: {self.road_event}, Day of week {self.day_of_week}, Day of month {self.day}, month of year {self.month}, year {self.year}")

    def get_row(self):
        return [self.id, self.timestamp, self.longtitudes, self.latitudes, self.velocity, self.duration, self.road_type, self.road_condition, self.road_event, self.hour, self.minute, self.day_of_week, self.day, self.month, self.year]

exports = []

def export_data():
    for v in vehicles:
        for l in lanes:
            if v.lane == l.id:
                v.lane = l.type
                v.condition = "smooth"
                

    for v in vehicles:
        exports.append(export(v.id, v.time, v.x, v.y, v.speed, v.duration, v.lane, v.condition, v.event, v.hour, v.minute, v.day_of_week, v.day, v.month, v.year))

    f = open('./data.csv', 'w')

    writer = csv.writer(f)

    writer.writerow(["Node", "Timestamp", "X", "Y", "Velocity", "Duration", "Road Type", "Road Condition", "Road Event", "Hour", "Minute", "Second", "Day Of Week", "Day", "Month", "Year"])

    for ve in exports:
        writer.writerow(ve.get_row())
    
    # for e in exports:
    #     e.display()

export_data()
