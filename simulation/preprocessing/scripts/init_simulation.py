input = "../../sumo/simulation.sumo.cfg"

with open(input) as file:
    
    lines = file.readlines()

    begin = 0
    end = 480
    times = 1

    while times < 366:

      for i in range(len(lines)):
        if '<begin value="' in lines[i]:
          temp = lines[i].split('"')
          temp[1] = str(begin)
          str_temp = '"'.join(temp)
          lines[i] = str_temp
          begin += 480
          
        elif '<end value="' in lines[i]:
          temp = lines[i].split('"')
          temp[1] = str(end)
          str_temp = '"'.join(temp)
          lines[i] = str_temp
          end += 480

      name_file = "../../sumo/simulation" + str(times) + ".sumo.cfg"
      new_file = open(name_file, "w")
      new_file.writelines(lines)
        
    times += 1
