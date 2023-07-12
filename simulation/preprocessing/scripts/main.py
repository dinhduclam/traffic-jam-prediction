# Begin 


import os

# init data of simulation
command = "python3 init_simulation.py"
os.system(command)

# init data of vehicle
command = "python3 init_vehicle.py"
os.system(command)

# convert xml data of vehicle to 
command = "python3 convert_data.py"
os.system(command)

