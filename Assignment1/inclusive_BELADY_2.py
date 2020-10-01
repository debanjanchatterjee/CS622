l2_cache=dict()
#l3_cache=dict()
l3_cache=set()
addr_seq=dict()
l3_unique_blocks=set()

i_count=1


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
    global l2_cache, l3_cache, addr_seq, l3_unique_blocks
    global l2_set_associativity

    #set_no = addr[47:58]
    tag = addr[0:58]



    if len(l3_cache)== 32768:                        # max capacity
        x=findBeladyReplacement(addr)                       #removed lru element
        l3_cache.remove(x)
        evictL2(addr)
        l3_cache.add(tag)
        l3_cache_lru.insert(0, tag)

    else:
        l3_cache.add(tag)
        l3_cache_lru.insert(0, tag)


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
    for t in addr_seq.keys():
        i=next(addr_seq[t], i_count)
        current_dist=addr_seq[t][i]-i_count
        if current_dist>max_dist:


    return x

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
    global l2_miss, l3_miss, l3_cold_miss, l3_capacity_miss, i_count
    global l2_cache, l3_cache
    global l2_set_associativity

    #set_no=addr[47:58]
    tag=addr[0:58]

    if tag in l3_cache:                                   #hit in l3 but miss in l2
        l3_cache_lru.remove(tag)
        l3_cache_lru.insert(0,tag)                          #maintaining lru order

    else:                                                   #miss in l3
        l3_miss=l3_miss+1
        if tag not in l3_unique_blocks:
            l3_cold_miss=l3_cold_miss+1
            l3_unique_blocks.add(tag)

        loadL3(addr)
        loadL2(addr)






def main():
    global l2_miss, l3_miss, l3_cold_miss, l3_capacity_miss
    global l2_cache, l3_cache, addr_seq
    global l2_set_associativity
    f = open("output.txt", "r")
    adrressspace=64
    Lines=f.readlines()
    count=1
    for l in Lines:
        token=l.split(',')
        type=int(token[0])
        address=int(token[1])
        addr=bin(address)[2:].zfill(64)          #processed adress
        if type!=0:
            #lookL2(addr)
            #addr_seq.append(addr)
            tag = addr[0:58]

            if tag in addr_seq.keys():
                addr_seq[tag].append(count)
            else:
                addr_seq[tag]=list()
            count=count+1


    for l in Lines:
        token=l.split(',')
        type=int(token[0])
        address=int(token[1])
        addr=bin(address)[2:].zfill(64)          #processed adress
        if type!=0:
            lookL2(addr)
            i_count=i_count+1


    print('L2 misses:'+str(l2_miss))
    print('L3 misses:'+str(l3_miss))
    print('L3 cold misses'+ str(l3_cold_miss))
    l3_capacity_miss=l3_miss-l3_cold_miss
    print('L3 capacity misses='+str(l3_capacity_miss))
    f.close()


if __name__ == "__main__":
    main()