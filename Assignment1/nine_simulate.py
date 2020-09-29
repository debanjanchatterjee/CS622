
l2_cache=dict()
l3_cache=dict()

l2_miss=0
l3_miss=0

#def initL2():



#def initL3():

def lookL2(addr):
    global l2_miss, l3_miss
    global l2_cache,l3_cache

    set_no=addr[48:58]
    tag=addr[0:48]

    if set_no in  l2_cache.keys():
        if tag in l2_cache[set_no]:                     #l2-hit
            

        else:
            l2_miss = l2_miss + 1
            lookL3(addr)
    else:
        l2_miss=l2_miss+1
        lookL3(addr)


def lookL3(addr):
    global l2_miss, l3_miss
    global l2_cache, l3_cache


    set_no=addr[47:58]
    tag=addr[0:47]





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