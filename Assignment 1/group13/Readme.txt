Steps to follow to execute the assignment:

System Specs:
Os:**Ubuntu**
4GB Ram

Language used: Python3


######################## download into traces folder ##########################      
1. Download all the trace files of the 6 applications from https://www.cse.iitk.ac.in/users/mainakc/2020Autumn/traces.zip and unzip them into a folder called traces.

######################## Input Processing #####################################
2. Execute the processtraces.py in inputProcess folder( go to -> inputProcess folder , execute python3 processtraces.py)
( this step reads type and address from traces and stores into separate .txt files)


######################## Problem 1 ############################################
3. Now go to Task1 folder.

4. Execute the inclusive_simulate.py ( python3 inclusive_simulate.py)
5. Generates a inclusive_ouput.txt file with L2 and L3 misses ( approximate time taken 6 mins)

6. Execute the nine_simulate.py ( python3 nine_simulate.py)
7. Generates a nine_ouput.txt file with L2 and L3 misses ( approximate time taken 5 mins)

8. Execute the exclusive_simulate.py ( python3 exclusive_simulate.py)
9. Generates a exclusive_ouput.txt file with L2 and L3 misses ( approximate time taken 5 mins)


######################## Problem 2 #############################################

10. Now go to Task2 folder.

11. Execute the inclusive_LRU_2.py file ( python3 inclusive_LRU_2.py)
12. Generates a inclusive_FA_Lru_output.txt file with L3 cold and capacity misses (approximate time taken 65mins)


13. Execute the inclusive_BELADY_2.py file ( python3 inclusive_BELADY_2.py)
14. Generates a inclusive_BELADY_output.txt file with L3 cold and capacity misses.

Note: as belady is a future reference policy, the looping through the cache blocks(2^15) with the whole list of address references slows it down.
      Each file gromacs: approx 80 mins
                hmmer  : approx 2.2 hrs
                h264ref: approx 61 mins
                bzip2  : approx 7 hrs
                gcc    : approx 7 hrs
                sphinx3 : >8.5 hrs
sphinx performs badly due to bad temporal and spatial locality.


#################################################################################
