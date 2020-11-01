import os


os.system("python3 acsdis_cache.py prog1.out")
os.system("python3 acsdis_cache.py prog2.out")
os.system("python3 acsdis_cache.py prog3.out")
os.system("python3 acsdis_cache.py prog4.out")

os.system("python3 access_distance.py mislsprog1.out")
os.system("python3 access_distance.py mislsprog2.out")
os.system("python3 access_distance.py mislsprog3.out")
os.system("python3 access_distance.py mislsprog4.out")


os.system("python3 cdf_plot.py mislsprog1_accessdistance.json")
os.system("python3 cdf_plot.py mislsprog2_accessdistance.json")
os.system("python3 cdf_plot.py mislsprog3_accessdistance.json")
os.system("python3 cdf_plot.py mislsprog4_accessdistance.json")


