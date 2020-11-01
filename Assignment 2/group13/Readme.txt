1) Download pin tool 3.15 and setup 
2)Create a directory named CS622Assignment under pin-3.15-98253-gb56e429b1-gcc-linux/source/tools/.
3)Copy prog1.c, prog2.c, prog3.c, prog4.c, makefile, makefile.rules into this directory.
4)Copy the contents of given assignment into the folder 

NOTE:[just copy the entire CS622 assignment folder submitted into the pin-3.15-98253-gb56e429b1-gcc-linux/source/tools/]


####################Problem1#########################################

5)execute the python3 script_ques1.py

6)the prog1.out,prog2.out,prog3.out,prog4.out has the necessary threadwise memory access trace (approx time taken:25-30mins)
7)the trace_count.out has the total count of traces in each of the binaries after passed through the addrtrace.cpp

#####################Problem2########################################
//Note: pip3 install matplotlib if not done


8)Execute python3 script_ques2.py (approx time taken:10mins)// outputs 4 json files  containing  the access_distance dictionary and its frequency
//also outputs 4 .png plots of cdf


//for verifying individual values by passing d
9) to execute the cumulative density function follow as below:
         a)python3 cumulative_density.py progtrace.json d_value 
         b)(example: python3 cumulative_density.py prog2_accessdistance.json 4)


####################### Problem3 ########################
10)Execute the python3 script_ques3.py (approx time taken:10mins)  //gives the misslist.out for each prog1,prog2,prog3,prog4 and the 4 json files as of question2 and 4.png files
//Also gives output q3output.txt which has hit and miss values of each trace


##################Problem4##############################
11) Execute python3 script_ques4.py  // sharing_profile.txt as the ouput
