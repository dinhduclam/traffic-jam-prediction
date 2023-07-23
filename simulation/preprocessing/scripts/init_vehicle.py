import os

times = 1
begin = 0
end = 480

PATH_RANDOMTRIP = "python3 /home/parallel_user/sumo/tools/randomTrips.py"
PATH_NET = "../../sumo/net.net.xml"
PATH_ROUTE = "../../sumo/route.rou.xml"

times = 1
while times < 2:
  command1 = PATH_RANDOMTRIP + " -n" + PATH_NET + " -r " + PATH_ROUTE +" -b " + str(begin) +  " -e " + str(end) + " -p 4 -l"

  os.system(command1)

  command2 = "sumo -c ../sumo/simulation" + str(times) + ".sumo.cfg --fcd-output ../sumo/data/vehicle" + str(times) +".sumo.xml --fcd-output.geo"

  os.system(command2)

  begin += 480
  end += 480
  times += 1