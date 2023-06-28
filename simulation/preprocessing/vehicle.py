# Define class vehicle

class vehicle:
    def __init__(self, _node, _x, _y , _z, _time):
        self.node = _node
        self.x = _x
        self.y = _y
        self.z = _z
        self.time = _time
    
    def display(self):
        print(f"Node: {self.node}, x: {self.x}, y: {self.y}, z: {self.z}, time: {self.time}")
    
    def get_row(self):
        return [self.node, self.x, self.y, self.z, self.time]
    
    def get_header(self):
        return ["Node", "X", "Y", "Z", "Time"]