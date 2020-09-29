
l2_cache=dict()
l3_cache=dict()

l2_miss=0
l3_miss=0

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
            l2_cache[set_no].insert(0,tag)
        else:
            l2_cache[set_no].insert(0,tag)
    else:
        l2_cache[set_no]=list()
        l2_cache[set_no].append(tag)

def loadL3(addr):
    global l2_miss, l3_miss
    global l2_cache, l3_cache
    global l2_set_associativity, l3_set_associativity

    set_no = addr[47:58]
    tag = addr[0:47]

    if set_no not in l3_cache.keys():
        if len(l3_cache[set_no])==l3_set_associativity:               #l3 set full
            

        else:
            l3_cache[set_no].insert(0,tag)

    else:
        l3_cache[set_no] = list()
        l3_cache[set_no].append(tag)






def lookL2(addr):
    global l2_miss, l3_miss
    global l2_cache, l3_cache
    global l2_set_associativity, l3_set_associativity
    set_no=addr[48:58]
    tag=addr[0:48]

    if set_no in  l2_cache.keys():
        if tag in l2_cache[set_no]:                     #l2-hit
            l2_cache[set_no].remove(tag)
            l2_cache[set_no].insert(0, tag)              #updated LRU status

        else:
            l2_miss = l2_miss + 1
            lookL3(addr)
    else:
        l2_miss=l2_miss+1
        lookL3(addr)



def lookL3(addr):
    global l2_miss, l3_miss
    global l2_cache, l3_cache
    global l2_set_associativity, l3_set_associativity

    set_no=addr[47:58]
    tag=addr[0:47]

    if set_no in l3_cache.keys():
        if tag in l3_cache[set_no]:



        else:
            l3_miss=l3_miss+1
            loadL3(addr)


    else:                         #miss in both l2 and l3
        l3_miss=l3_miss+1

        #l3_cache[set_no]=list()
        #l3_cache[set_no].append(tag)
        loadL3(addr)
        loadL2(addr)                            #load in l2 cache







def main():
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


    f.close()


if __name__ == "__main__":
    main()