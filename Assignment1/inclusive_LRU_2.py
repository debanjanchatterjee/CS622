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
        evictL2(addr)
        l3_cache.add(tag)
        l3_cache_lru.insert(0, tag)

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
    f = open("output.txt", "r")
    adrressspace=64
    Lines=f.readlines()
    for l in Lines:
        token=l.split(',')
        type=int(token[0])
        address=int(token[1])
        addr=bin(address)[2:].zfill(64)          #processed adress
        if type!=0:
            lookL2(addr)


    print('L2 misses:'+str(l2_miss))
    print('L3 misses:'+str(l3_miss))
    print('L3 cold misses'+ str(l3_cold_miss))
    l3_capacity_miss=l3_miss-l3_cold_miss
    print('L3 capacity misses='+str(l3_capacity_miss))
    f.close()


if __name__ == "__main__":
    main()