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
#l3_cache=dict()
l3_cache=set()
l3_cache_lru=list()
l3_unique_blocks=set()


l2_miss=0
l3_miss=0
l3_capacity_miss=0
l3_cold_miss=0

l2_set_associativity=8
#l3_set_associativity=16

#def initL2():



#def initL3():


def loadL2(addr):
    global l2_miss, l3_miss
    global l2_cache, l3_cache
    global l2_set_associativity

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
    global l2_miss, l3_miss
    global l2_cache, l3_cache, l3_cache_lru, l3_unique_blocks
    global l2_set_associativity

    #set_no = addr[47:58]
    tag = addr[0:58]



    if len(l3_cache)== 32768:                        # max capacity
        x=l3_cache_lru.pop()
        l3_cache.remove(x)                          #removed lru element
        
        l3_cache.add(tag)
        l3_cache_lru.insert(0, tag)
        evictL2(x)
    else:
        l3_cache.add(tag)
        l3_cache_lru.insert(0, tag)



def evictL2(addr):
    global l2_miss, l3_miss
    global l2_cache, l3_cache, l3_cache_lru, l3_unique_blocks
    global l2_set_associativity

    set_no = addr[48:58]
    tag = addr[0:48]

    if set_no in l2_cache.keys():
        if tag in l2_cache[set_no]:                                    #block also present in l2
            l2_cache[set_no].remove(tag)







def lookL2(addr):
    global l2_miss, l3_miss
    global l2_cache, l3_cache
    global l2_set_associativity
    set_no=addr[48:58]
    tag=addr[0:48]

    if set_no in  l2_cache.keys():
        if tag in l2_cache[set_no]:                     #l2-hit
            l2_cache[set_no].remove(tag)
            l2_cache[set_no].insert(0, tag)              #updated LRU status

        else:
            l2_miss = l2_miss + 1                         #l2 miss
            lookL3(addr)
    else:                                                  #l2 miss
        l2_miss=l2_miss+1
        lookL3(addr)



def lookL3(addr):
    global l2_miss, l3_miss, l3_cold_miss, l3_capacity_miss
    global l2_cache, l3_cache, l3_cache_lru
    global l2_set_associativity

    #set_no=addr[47:58]
    tag=addr[0:58]

    if tag in l3_cache:                                   #hit in l3 but miss in l2
        l3_cache_lru.remove(tag)
        l3_cache_lru.insert(0,tag)
        loadL2(addr)                          #maintaining lru order

    else:                                                   #miss in l3
        l3_miss=l3_miss+1
        if tag not in l3_unique_blocks:
            l3_cold_miss=l3_cold_miss+1
            l3_unique_blocks.add(tag)

        loadL3(addr)
        loadL2(addr)






def main():
    global l2_miss, l3_miss, l3_cold_miss, l3_capacity_miss,l2_cache,l3_cache,l3_cache_lru,l3_unique_blocks
    
    adrressspace=64
    for t in allTraces:
            start=time.time()
            files=allTraces[t]
            l2_cache=dict()
            l3_cache=set()
            l3_cache_lru=list()
            l3_unique_blocks=set()


            l2_miss=0
            l3_miss=0
            l3_capacity_miss=0
            l3_cold_miss=0

            print('Executing  Trace : '+ t )
            
            for fil in files:
                 with open(fil) as f:
                       for line in f:
                             l=line.split(' ');
                             
                             types=int(l[0])
                             addr=int(l[1])
                             addr=bin(addr)[2:].zfill(64)  
                             
                             if(types):
                             	lookL2(addr)
            print('L3 cold misses'+ str(l3_cold_miss))
            l3_capacity_miss=l3_miss-l3_cold_miss
            print('L3 capacity misses='+str(l3_capacity_miss))
            print('time taken : ',time.time()-start)
            print()
            with open('inclusive_FA_Lru_output.txt', 'a') as s:
                s.write('Executing Trace : %s\n '% t )
                s.write("L3 cold Miss:  %s\n" % l3_cold_miss)
                s.write("L3 capacity  Miss: %s\n" % l3_capacity_miss)
                s.write("time taken in seconds: %s\n"% str(time.time()-start))
                s.write(".......................................................\n\n")
            
            
    
    


if __name__ == "__main__":
    main()
