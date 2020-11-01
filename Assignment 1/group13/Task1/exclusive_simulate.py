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
	#emptylist=[]
	l2cache=dict()
	#for setno in range(1024):
	#	l2cache[bin(setno)[2:].zfill(10)]=emptylist
	return l2cache


def initialiseL3Cache():
	#emptylist=[]
	l3cache=dict()
	#for setno in range(2048):
	#	l3cache[bin(setno)[2:].zfill(11)]=emptylist
	return l3cache



	
def findinL2Cache(address):
	global l2cache,l2miss,l2hit
	l2tag=address[:48]
	l2index=address[48:58]
	if l2index in l2cache.keys():
		if l2tag in l2cache[l2index]:
			l2hit+=1
			l2cache[l2index].remove(l2tag)
			l2cache[l2index].insert(0,l2tag)
		else:
			l2miss+=1
			findinL3Cache(address)
	else:
		l2miss+=1
		findinL3Cache(address)


def findinL3Cache(address):
	global l3cache,l3hit,l3miss
	l3tag=address[:47]
	l3index=address[47:58]
	if l3index in l3cache.keys():
		if l3tag in l3cache[l3index]:
			l3hit+=1
			l3cache[l3index].remove(l3tag)
			insertintoL2Cache(address)
		else:
			l3miss+=1
			insertintoL2Cache(address)
	else:
		l3miss+=1
		#insertintoL3Cache(address)
		insertintoL2Cache(address)



def insertintoL2Cache(address):
	global l2cache,L2Assoc
	l2tag=address[:48]
	l2index=address[48:58]
	evictedaddress=""
	if l2index in l2cache.keys():
		if len(l2cache[l2index])<L2Assoc:
			l2cache[l2index].insert(0,l2tag)
		else:
			evictedaddress=l2cache[l2index].pop()+l2index
			l2cache[l2index].insert(0,l2tag)
			insertintoL3Cache(evictedaddress)
	else:
	
		l2cache[l2index] = list()
		l2cache[l2index].append(l2tag)






def insertintoL3Cache(address):
	global l3cache,L3Assoc
	l3tag=address[:47]
	l3index=address[47:58]
	if l3index in l3cache.keys():
		if len(l3cache[l3index])<L3Assoc:
			l3cache[l3index].insert(0,l3tag)
		else:
			l3cache[l3index].pop()
			l3cache[l3index].insert(0,l3tag)
	else:
		l3cache[l3index] = list()
		l3cache[l3index].append(l3tag)


def main():
        global l2cache,l3cache,l2miss,l3miss,l2hit,l3hit,L2Assoc,L3Assoc
        
        L2Assoc=8
        L3Assoc=16
       
        for t in allTraces:
            l2cache=initialiseL2Cache()
            l3cache=initialiseL3Cache()
            l2miss=l3miss=l2hit=l3hit=0
            start=time.time()
            print('Executing on Trace : '+ t )
            files=allTraces[t]
            for fil in files:
                 with open(fil) as f:
                       for line in f:
                             l=line.split(' ');
                             types=int(l[0])
                             addr=int(l[1])
                             if(types):
                             	findinL2Cache(bin(addr)[2:].zfill(64))
            print("L2Miss:",l2miss,"and\t","L2Hit:",l2hit)
            print("L3Miss:",l3miss,"and\t","L3Hit:",l3hit)
            print("time taken:",time.time()-start)
            with open('exclusive_output.txt', 'a') as s:
                s.write('Executing Trace : %s\n '% t )
                s.write("L2Miss:  %s\n" % l2miss)
                s.write("L3 Miss: %s\n" % l3miss)
                s.write("time taken in seconds: %s\n"% str(time.time()-start))
                s.write(".......................................................\n\n")
        
        
        
if __name__ == "__main__":
    main()

