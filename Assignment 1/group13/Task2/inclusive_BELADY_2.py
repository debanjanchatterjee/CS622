import time

allTraces = {
	
	'gromacs':['../traces/gromacs.log_l1misstrace.text_0'],
	'h264ref':['../traces/h264ref.log_l1misstrace.text_0'],
	'hmmer':  ['../traces/hmmer.log_l1misstrace.text_0'],
	'bzip'	: ['../traces/bzip2.log_l1misstrace.text_0','../traces/bzip2.log_l1misstrace.text_1'],
	'gcc':    ['../traces/gcc.log_l1misstrace.text_0','../traces/gcc.log_l1misstrace.text_1'],
	'sphinx3':['../traces/sphinx3.log_l1misstrace.text_0','../traces/sphinx3.log_l1misstrace.text_1']
	
	
	
	}


l2_cache=dict()
l3_cache=set()
addr_seq=dict()
l3_unique_blocks=set()

i_count=1


l2_miss=0
l3_miss=0
l3_capacity_miss=0
l3_cold_miss=0

l2_set_associativity=8


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
    global l2_cache, l3_cache, addr_seq, l3_unique_blocks
    global l2_set_associativity

    #set_no = addr[47:58]
    tag = addr[0:58]



    if len(l3_cache)== 32768:                        # max capacity
        x=findBeladyReplacement(addr)                       #removed lru element
        l3_cache.remove(x)
        evictL2(x)
        l3_cache.add(tag)

    else:
        l3_cache.add(tag)


def next(arr, target):
    start = 0
    end = len(arr) - 1

    ans = -1
    while (start <= end):
        mid = (start + end) // 2

        # Move to right side if target is
        # greater.
        if (arr[mid] <= target):
            start = mid + 1

        # Move left side.
        else:
            ans = mid
            end = mid - 1

    return ans

def findBeladyReplacement(addr):
    global l2_miss, l3_miss, i_count
    global l2_cache, l3_cache,addr_seq , l3_unique_blocks
    global l2_set_associativity

    # set_no = addr[47:58]
    tag = addr[0:58]

    if tag not in addr_seq.keys():
        print('logical error')
    max_dist=-1
    x=None
    for t in l3_cache:
        i=next(addr_seq[t], i_count)
        if i==-1:
            return t
        current_dist=addr_seq[t][i]-i_count
        if current_dist>max_dist:
            max_dist=current_dist
            x=t
    return x


def evictL2(addr):
    global l2_miss, l3_miss
    global l2_cache, l3_cache, addr_seq, l3_unique_blocks
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
    global l2_miss, l3_miss, l3_cold_miss, l3_capacity_miss, i_count
    global l2_cache, l3_cache, addr_seq
    global l2_set_associativity

    #set_no=addr[47:58]
    tag=addr[0:58]

    if tag in l3_cache:                                   #hit in l3 but miss in l2
       
        loadL2(addr)

    else:                                                   #miss in l3
        l3_miss=l3_miss+1
        if tag not in l3_unique_blocks:
            l3_cold_miss=l3_cold_miss+1
            l3_unique_blocks.add(tag)

        loadL3(addr)
        loadL2(addr)






def main():

   global l2_miss, l3_miss, l3_cold_miss, l3_capacity_miss, i_count
   global l2_cache, l3_cache, addr_seq
   global l2_set_associativity
   for t in allTraces:
    count = 1
    start=time.time()   
    l2_cache=dict()
    l3_cache=set()
    addr_seq=dict()
    l3_unique_blocks=set()

    i_count=1
    total=0

    l2_miss=0
    l3_miss=0
    l3_capacity_miss=0
    l3_cold_miss=0
    files=allTraces[t]
    print("Executing trace:",t)
    for fil in files:
       with open(fil) as f:
        for line in f:
            tokn=line.split(' ')
            
            types=int(tokn[0])
            address=int(tokn[1])
            addr=bin(address)[2:].zfill(64)          #processed adress
            if types!=0:
                tag = addr[0:58]

                if tag in addr_seq.keys():
                    addr_seq[tag].append(count)
                else:
                    addr_seq[tag]=list()
                count=count+1
        f.close()

    for fi in files:
       with open(fi) as m:
        for l in m:
            token=l.split(' ')
            types=int(token[0])
            address=int(token[1])
            addr=bin(address)[2:].zfill(64)          #processed adress
            total+=1
            if types!=0:
                lookL2(addr)
                i_count=i_count+1
        f.close()

    print('total',total)
    print('L2 misses:'+str(l2_miss))
    print('L3 misses:'+str(l3_miss))
    print('L3 cold misses'+ str(l3_cold_miss))
    l3_capacity_miss=l3_miss-l3_cold_miss
    print('L3 capacity misses='+str(l3_capacity_miss))
    print('time taken',time.time()-start)
    with open('inclusive_FA_Belady_output.txt', 'a') as s:
                s.write('Executing Trace : %s\n '% t )
                s.write("L3 cold Miss:  %s\n" % l3_cold_miss)
                s.write("L3 capacity  Miss: %s\n" % l3_capacity_miss)
                s.write("time taken in seconds: %s\n"% str(time.time()-start))
                s.write(".......................................................\n\n")
            
   


if __name__ == "__main__":
    main()
