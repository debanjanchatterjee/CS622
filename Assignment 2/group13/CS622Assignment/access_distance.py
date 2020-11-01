import time
import json
import collections
import sys


acsdis=dict()
memblk=dict()
count=0
m=0
a=0
def accessdistance(address,c):
	global acsdis,memblk,count,m,a
	val=0
	if address in memblk.keys():
		val=c-memblk[address]
		memblk[address]=c
		if val in acsdis.keys():
			acsdis[val]+=1
		else:
			acsdis[val]=1
		a+=1
	else:
		memblk[address]=c
		m+=1
def main():
        global acsdis,memblk,count,m,a
        if len(sys.argv) != 2:
                   print("please enter the correct trace file to continue")
                   exit()
        else:
                 print("executing the trace",sys.argv[1])
                 fil=sys.argv[1]
                 count=0
                 with open(fil) as f:
                       for line in f:
                             token=line.split(' ');
                             tid=int(token[0])
                             addres=int(token[1])
                             addr=(addres-(addres%64))
                             count+=1
                             accessdistance(addr,count)
                             
                       od = collections.OrderedDict(sorted(acsdis.items()))
                       od['total']=a
                       outfile=str(fil.split(".")[0])+"_accessdistance.json"
                       with open(outfile,'w') as g:
                       	#for key,value in acsdis.items():
                       		g.write(json.dumps(od))                          
                       print("total",count,"\tno of unique mem blocks",m,"\n no of access distances",a) 
                       print("no of unique access distances",len(acsdis))
                             
                
        
if __name__ == "__main__":
    main()

