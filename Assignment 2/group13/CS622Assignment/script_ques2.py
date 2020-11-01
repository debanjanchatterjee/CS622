import os




os.system("python3 access_distance.py prog1.out")
os.system("python3 access_distance.py prog2.out")
os.system("python3 access_distance.py prog3.out")
os.system("python3 access_distance.py prog4.out")

os.system("python3 cdf_plot.py prog1_accessdistance.json")
os.system("python3 cdf_plot.py prog2_accessdistance.json")
os.system("python3 cdf_plot.py prog3_accessdistance.json")
os.system("python3 cdf_plot.py prog4_accessdistance.json")

