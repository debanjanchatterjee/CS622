import json
import matplotlib.pyplot as plt
import math
import sys


def main():
	xlist=list()
	ylist=list() 
	if len(sys.argv) != 2:
		print("please enter the correct trace file to continue")
		exit()
	else:
		print("executing the trace",sys.argv[1])
		fil=sys.argv[1]
		with open(fil) as json_file: 
			data = json.load(json_file)
			res=0
			total=data['total']
			del data['total'] 
			for key,value in data.items():
				xlist.append(math.log10(int(key)))
				res+=value
				ylist.append((res/total))
			plt.plot(xlist, ylist) 
  
			plt.xlabel('access-distance') 
			plt.ylabel('cumulative density function') 
  
			plt.title(str(fil.split(".")[0])) 
			figname=str(fil.split(".")[0])+".png"  
			plt.savefig(figname) 	
	  
if __name__ == "__main__":
    main()
