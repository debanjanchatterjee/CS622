import time
import sys

	
cache=dict()
hit=miss=0
Cachemisslist=list()	
def findincache(addre):
	global hit,miss,cache,Cachemisslist
	address=bin(addre)[2:].zfill(64)
	tag=address[:47]
	index=address[47:58]
	if index in cache.keys():
		if tag in cache[index]:
			hit+=1
			cache[index].remove(tag)
			cache[index].insert(0,tag)
		else:
			miss+=1
			Cachemisslist.append(addre)
		
			insertincache(address)
	else:
		miss+=1
		Cachemisslist.append(addre)
		insertincache(address)
	


def insertincache(address):
	global cache
	index=address[47:58]
	tag=address[:47]
	if index in cache.keys():
		if len(cache[index])<16:
			cache[index].insert(0,tag)
		else:
			
			cache[index].pop()
			cache[index].insert(0,tag)		
		
	else:
		cache[index] = list()
		cache[index].append(tag)
	


def main():
        global cache,hit,miss,Cachemisslist
        if len(sys.argv) != 2:
                   print("please enter the correct trace file to continue")
                   exit()
        else:
        
        
            fil=sys.argv[1]
            print('Executing Trace : ', fil )
            
            
            with open(fil) as f:
                       for line in f:
                             token=line.split(' ');
                             tid=int(token[0])
                             addres=int(token[1])
                             #addr=(addres-(addres%64))
                             findincache(addres)
            
            
            
            
            
            
            ####to write
            outfile="q3output.txt"
            with open(outfile, 'a') as s:
                s.write('Executing Trace : %s\n'% fil )
                s.write("Miss:  %s\n" % miss)
                s.write("hit: %s\n" % hit)
                #s.write("time taken in seconds: %s\n"% str(time.time()-start))
                s.write(".......................................................\n\n")
            missfile="misls"+str(fil.split(".")[0])+".out"
            with open(missfile,'a') as m:
                ini=0 
                for item in Cachemisslist:
                  m.write("%d %s\n" % (ini,item))
        
if __name__ == "__main__":
    main()

