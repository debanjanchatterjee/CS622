import os


os.system("gcc -O3 -static -pthread prog1.c -o prog1")
os.system("gcc -O3 -static -pthread prog2.c -o prog2")
os.system("gcc -O3 -static -pthread prog3.c -o prog3")
os.system("gcc -O3 -static -pthread prog4.c -o prog4")


os.system("mkdir obj-intel64")
os.system("make obj-intel64/addrtrace.so")
os.system("../../../pin -t obj-intel64/addrtrace.so -- ./prog1 8")
os.system("../../../pin -t obj-intel64/addrtrace.so -- ./prog2 8")
os.system("../../../pin -t obj-intel64/addrtrace.so -- ./prog3 8")
os.system("../../../pin -t obj-intel64/addrtrace.so -- ./prog4 8")

