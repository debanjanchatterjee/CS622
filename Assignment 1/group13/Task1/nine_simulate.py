import time
allTraces = {
	
	'bzip'	: ['../traces/bzip2.log_l1misstrace.text_0','../traces/bzip2.log_l1misstrace.text_1'],
	'gcc':    ['../traces/gcc.log_l1misstrace.text_0','../traces/gcc.log_l1misstrace.text_1'],
	'gromacs':['../traces/gromacs.log_l1misstrace.text_0'],
	'h264ref':['../traces/h264ref.log_l1misstrace.text_0'],
	'hmmer':  ['../traces/hmmer.log_l1misstrace.text_0'],
	'sphinx3':['../traces/sphinx3.log_l1misstrace.text_0','../traces/sphinx3.log_l1misstrace.text_1']
	
	
	
	}
l2_cache=dict()
l3_cache=dict()

l2_miss=0
l3_miss=0
l2hit=0
l3hit=0
l2_set_associativity=8
l3_set_associativity=16

#def initL2():



#def initL3():


def loadL2(addr):
    global l2_miss, l3_miss
    global l2_cache, l3_cache
    global l2_set_associativity, l3_set_associativity

    set_no = addr[48:58]
    tag = addr[0:48]

    if set_no in l2_cache.keys():                # set exists in l2 cache
        if len(l2_cache[set_no])==l2_set_associativity:           #set full
            l2_cache[set_no].pop()                                #removed LRU block
            l2_cache[set_no].insert(0, tag)
        else:
            l2_cache[set_no].insert(0, tag)
    else:
        l2_cache[set_no]=list()
        l2_cache[set_no].append(tag)

def loadL3(addr):
    global l2_miss, l3_miss,l3hit,l2hit
    global l2_cache, l3_cache
    global l2_set_associativity, l3_set_associativity

    set_no = addr[47:58]
    tag = addr[0:47]

    if set_no in l3_cache.keys():
        if len(l3_cache[set_no])==l3_set_associativity:               #l3 set full
            l3_cache[set_no].pop()
            l3_cache[set_no].insert(0,tag)                             #added block

        else:
            l3_cache[set_no].insert(0,tag)

    else:
        l3_cache[set_no] = list()
        l3_cache[set_no].append(tag)






def lookL2(addr):
    global l2_miss, l3_miss,l2hit,l3hit
    global l2_cache, l3_cache
    global l2_set_associativity, l3_set_associativity
    set_no=addr[48:58]
    tag=addr[0:48]

    if set_no in  l2_cache.keys():
        if tag in l2_cache[set_no]:                     #l2-hit
            l2_cache[set_no].remove(tag)
            l2_cache[set_no].insert(0, tag)
            l2hit+=1              #updated LRU status

        else:
            l2_miss = l2_miss + 1                         #l2 miss
            lookL3(addr)
    else:                                                  #l2 miss
        l2_miss=l2_miss+1
        lookL3(addr)



def lookL3(addr):
    global l2_miss, l3_miss,l3hit
    global l2_cache, l3_cache
    global l2_set_associativity, l3_set_associativity

    set_no=addr[47:58]
    tag=addr[0:47]

    if set_no in l3_cache.keys():
        if tag in l3_cache[set_no]:                           #hit in L3 but miss in L2
            l3_cache[set_no].remove(tag)
            l3_cache[set_no].insert(0, tag)
            l3hit+=1                  #updated LRU status
            loadL2(addr)

        else:                                                #miss in both l2 and l3
            l3_miss=l3_miss+1
            loadL3(addr)
            loadL2(addr)
    else:                                                    #miss in both l2 and l3
        l3_miss=l3_miss+1
        loadL3(addr)
        loadL2(addr)                                             #load in l2 cache







def main():
   global l2_miss, l3_miss,l2hit,l3hit,l2_cache,l3_cache
   
   
   for t in allTraces:
            l2_miss=l3_miss=l2hit=l3hit=0
            l2_cache=dict()
            l3_cache=dict()
            print('Executing on Trace : '+ t )
            start=time.time()
            files=allTraces[t]
            total=0
            adrressspace=64
            for fil in files:
                 with open(fil) as f:
                       for l in f:
                             token=l.split(' ')
                             type=int(token[0])
                             address=int(token[1])
                             addr=bin(address)[2:].zfill(64)          #processed adress
                             if type!=0:
                               lookL2(addr)

        
            print('L2 misses:',l2_miss,'\tL2 hit:',l2hit)
            print('L3 misses:',l3_miss,'\tL3 hit:',l3hit)
            print('time taken:\t',time.time()-start)
            with open('nine_output.txt', 'a') as s:
                s.write('Executing Trace : %s\n '% t )
                s.write("L2Miss:  %s\n" % l2_miss)
                s.write("L3 Miss: %s\n" % l3_miss)
                s.write("time taken in seconds: %s\n"% str(time.time()-start))
                s.write(".......................................................\n\n")

if __name__ == "__main__":
    main()
