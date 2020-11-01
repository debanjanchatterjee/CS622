import time
allTraces = {
	
	
	'bzip'	: ['../traces/bzip2.log_l1misstrace.text_0','../traces/bzip2.log_l1misstrace.text_1'],
	'gcc':    ['../traces/gcc.log_l1misstrace.text_0','../traces/gcc.log_l1misstrace.text_1'],
	'gromacs':['../traces/gromacs.log_l1misstrace.text_0'],
	'h264ref':['../traces/h264ref.log_l1misstrace.text_0'],
	'hmmer':  ['../traces/hmmer.log_l1misstrace.text_0'],
	'sphinx3':['../traces/sphinx3.log_l1misstrace.text_0','../traces/sphinx3.log_l1misstrace.text_1']
	
	
	
	}
def initialiseL2Cache():
	l2cache=dict()
	return l2cache


def initialiseL3Cache():
	l3cache=dict()
	return l3cache



	
def findinL2Cache(address):
	global l2cache,l2miss,l2hit,L2missList
	l2tag=address[:48]
	l2index=int(address[48:58],2)%1024
	if l2index in l2cache.keys():
		if l2tag in l2cache[l2index]:
			l2hit+=1
			l2cache[l2index].remove(l2tag)
			l2cache[l2index].insert(0,l2tag)
		else:
			l2miss+=1
			L2missList.append(address)
			findinL3Cache(address)
	else:
		l2miss+=1
		L2missList.append(address)
		findinL3Cache(address)
	



def findinL3Cache(address):
	global l3cache,l3miss,l3hit
	l3tag=address[:47]
	l3index=int(address[47:58],2)%2048
	if l3index in l3cache.keys():
		if l3tag in l3cache[l3index]:
			l3cache[l3index].remove(l3tag)
			l3cache[l3index].insert(0,l3tag)
			l3hit+=1
			insertintoL2Cache(address)
		else:
			l3miss+=1
			insertintoL3Cache(address)
			insertintoL2Cache(address)
		
		
	else:
		l3miss+=1
		insertintoL3Cache(address)
		insertintoL2Cache(address)
	




def insertintoL2Cache(address):
	global l2cache,L2Assoc
	l2index=int(address[48:58],2)%1024
	l2tag=address[:48]
	if l2index in l2cache.keys():
		if len(l2cache[l2index])<L2Assoc:
			l2cache[l2index].insert(0,l2tag)
		else:
			
			l2cache[l2index].pop()
			l2cache[l2index].insert(0,l2tag)		
		
	else:
		l2cache[l2index] = list()
		l2cache[l2index].append(l2tag)
	






def insertintoL3Cache(address):
	global l3cache,L3Assoc
	evictedaddress=0
	l3tag=address[:47]
	l3index=int(address[47:58],2)%2048
	if l3index in l3cache.keys():
		if len(l3cache[l3index])<L3Assoc:
			l3cache[l3index].insert(0,l3tag)
		else:
			evictedaddress=l3cache[l3index].pop()
			evictedaddress+=bin(l3index)[2:].zfill(11)
			l3cache[l3index].insert(0,l3tag)
			evictfromL2Cache(evictedaddress)
		
	
	else:
		l3cache[l3index] = list()
		l3cache[l3index].append(l3tag)
	





def evictfromL2Cache(address):
	global l2cache
	l2index=int(address[48:58],2)%1024
	l2tag=address[:48]
	if l2index in l2cache.keys():
		if l2tag in l2cache[l2index]:
			l2cache[l2index].remove(l2tag)
	else:
		print("l2index not fount while evicting")


def main():
        global l2cache,l3cache,l2miss,l3miss,l2hit,l3hit,L2Assoc,L3Assoc,L2missList
        L2Assoc=8
        L3Assoc=16
        for t in allTraces:
            start=time.time()
            L2missList=list()
            l2cache=initialiseL2Cache()
            l3cache=initialiseL3Cache()
            l2miss=l3miss=l2hit=l3hit=0
            print('Executing Trace : ', t )
            files=allTraces[t]
            for fil in files:
                 with open(fil) as f:
                       for line in f:
                             token=line.split(' ');
                             types=int(token[0])
                             addr=int(token[1])
                             
                             if(types):
                             	findinL2Cache(bin(addr)[2:].zfill(64))
            	
            print("L2Miss:",l2miss,"and\t","L2Hit:",l2hit)
            print("L3Miss:",l3miss,"and\t","L3Hit:",l3hit)
            print("time taken:",time.time()-start)
            with open('inclusive_output.txt', 'a') as s:
                s.write('Executing Trace : %s\n '% t )
                s.write("L2Miss:  %s\n" % l2miss)
                s.write("L3 Miss: %s\n" % l3miss)
                s.write("time taken in seconds: %s\n"% str(time.time()-start))
                s.write(".......................................................\n\n")
                
        
if __name__ == "__main__":
    main()

