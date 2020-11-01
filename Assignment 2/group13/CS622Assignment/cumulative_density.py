import json
import sys
###add total also into json dict with key as total

def main():
	if len(sys.argv) != 3:
		print("please enter the  trace file and d-value to continue")
		exit()
	else:
		print("executing the trace",sys.argv[1])
		fil=sys.argv[1]
		dval=sys.argv[2]	
		with open(fil) as json_file: 
			data = json.load(json_file)
			res=0
			total=data['total']
			del data['total'] 
			for key,value in data.items():
				if int(key) <= int(dval) :
					res+=value
				else:
					break
			print("cumulative value F(d)=n/N is : ",res/total)
if __name__ == "__main__":
    main()
