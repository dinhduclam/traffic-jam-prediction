import json
import csv

net_file = './data/net.json'
vehicle_file = './data/vehicle.json'


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
        
    # for l in lanes:
    #     print(l.id)

class vehicle:
    def __init__(self, _time, _id, _x, _y, _angle, _speed, _pos, _lane, _duration, _condition):
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
                       j['lane'], 0.0, "None"))
        elif (type(i['vehicle']) == dict):
            vehicles.append(vehicle(i['time'], i['vehicle']['id'], i['vehicle']['x'], i['vehicle']['y'], 
                       i['vehicle']['angle'], i['vehicle']['speed'], i['vehicle']['pos'], 
                       i['vehicle']['lane'], 0.0, "None"))

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

    # for v in new_vehicles:
    #     checked = set()
    #     for i in range(0, len(v)):
    #         for j in range(i + 1, len(v)):
    #             timestep = round (float(v[j].time) - float(v[i].time), 2)
    #             if timestep == 0.1 and v[i].id == v[j].id and v[i].pos == v[j].pos and v[i].id not in checked:
    #                 v[j].duration = round(float (v[j].time) - float(v[i].time), 2)
    #                 checked.add(v[i])

    for v in new_vehicles:
        duration = 0
        for i in range(1, len(v)):
            if v[i].pos == v[i-1].pos:
                duration += 0.1
        print(v[0].id, duration)


    # for v in new_vehicles:
    #     for e in v:
    #         if e.duration != 0:
    #             e.display()
    


class export: 
    def __init__(self, _id, _timestamp, _X, _Y, _velocity, _duration, _road_type, _road_condition, _road_event):
        self.id = _id
        self.timestamp = _timestamp
        self.latitudes = _X
        self.longtitudes = _Y
        self.velocity = _velocity
        self.duration = _duration
        self.road_type = _road_type
        self.road_condition = _road_condition
        self.road_event = _road_event

    def display(self):
        print(f"ID: {self.id} Timestamp: {self.timestamp}, Longtitudes: {self.longtitudes}, Latitudes: {self.latitudes}, velocity: {self.velocity}, duration: {self.duration}, road type: {self.road_type}, road condition: {self.road_condition}. road event: {self.road_event}")

    def get_row(self):
        return [self.id, self.timestamp, self.longtitudes, self.latitudes, self.velocity, self.duration, self.road_type, self.road_condition, self.road_event]

exports = []

def export_data():
    for v in vehicles:
        for l in lanes:
            if v.lane == l.id:
                v.lane = l.type
                v.condition = "smooth"
                

    for v in vehicles:
        exports.append(export(v.id, v.time, v.x, v.y, v.speed, v.duration, v.lane, v.condition, "None"))

    f = open('./data.csv', 'w')

    writer = csv.writer(f)

    writer.writerow(["Node", "Timestamp", "Latitudes", "Longtitudes", "Velocity", "Duration", "Road Type", "Road Condition", "Road Event"])

    for ve in exports:
        writer.writerow(ve.get_row())
    
    # for e in exports:
    #     e.display()

export_data()