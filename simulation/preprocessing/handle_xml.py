import json
import xmltodict
import os


input_file = '../simulation/sumo/net.net.xml'
# input_file = '../simulation/sumo/road-side.poly.xml'
# input_file = '../simulation/sumo/route.rou.xml'
# input_file = '../simulation/sumo/vehicle.sumo.xml'

output_file = './data/net.json'
# output_file = './data/road_side.json'
# output_file = './data/route.json'
# output_file = './data/vehicle.json'

temp = "Temp.json"
with open(input_file) as xml_file:
    data_dict = xmltodict.parse(xml_file.read())
    # xml_file.close()
        
    # generate the object using json.dumps()
    # corresponding to json data
        
    json_data = json.dumps(data_dict)
        
    # Write the json data to output
    # json file
    with open(temp, "w") as json_file:
        json_file.write(json_data)



# Delete @ character in file
fin = open(temp, "rt")
fout = open(output_file, "wt")
for line in fin:
	fout.write(line.replace('@', ''))
fin.close()
fout.close()

os.remove(temp)