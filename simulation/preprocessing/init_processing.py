from vehicle import *
import numpy as np
import csv

file = open('../simulation/init.tcl', 'r')

# Read the contents of the file
lines = file.readlines()
count = 0
# Print the contents to the console

string_list = []
vehicle_list = []

# preprocessing data from file init.tcl 
for line in lines:
    for i in range(len(line)):
        # tach cac tu trong chuoi bang khoang trang
        string_list = line.split(" ")
        for j in range(len(string_list)):
            
            # Delete string \n
            if "\n" in string_list[j]:
                string_list[j] = string_list[j].replace("\n","")
            # Delete string ""
            if "\"" in string_list[j]:
                string_list[j] = string_list[j].replace("\"","")

    vehicle_list.append(string_list)
    
vehicles_process = []

# Khoi tao gia tri x, y ,z cua cac phuong tien
x = 0
y = 0
z = 0

# Khoi tao gia tri bien dem so lan lap qua trang thai khoi tao
count = 0

# Set cac gia tri khi di xe cua mang vehicle_list
for v in vehicle_list:
    # Dong chua "setdest" dau tien luon la trang thai khoi tao cua 1 node
    # Cac dong "setdest" tiep theo la trang thai di xe cua 1 node
    if "setdest" in v:
        count = 0
        # print(f"{v} la trang thai di xe")
        new_vehicle = vehicle(v[3], v[5], v[6], v[7], v[2])
        vehicles_process.append(new_vehicle)

# df = pd.read_csv("./test.csv")
# print(df.head())
# df.to_csv("./test.csv", index=False)
f = open('./data.csv', 'w')

writer = csv.writer(f)

writer.writerow(["Node", "X", "Y", "Z", "Time"])

for ve in vehicles_process:
    writer.writerow(ve.get_row())

file.close()