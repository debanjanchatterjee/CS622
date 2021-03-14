import sys

def main():
	global inputQ0,inputQ1,inputQ2,inputQ3,inputQ4,inputQ5,inputQ6,inputQ7,cycle,globalid,L2msgcount,l2miss,L1msgcount,l1miss
	global l10cache,l11cache,l13cache,l14cache,l15cache,l16cache,l17cache,l12cache,cacheaccess,hitmiss,l1cacheaccess,l2cacheaccess,l2cache
	inputQ1=list();inputQ2=list();inputQ3=list();inputQ4=list();inputQ5=list();inputQ6=list();inputQ7=list();inputQ0=list();
	cycle=0
	globalid=0
	if len(sys.argv) != 2:
		print("please enter the correct trace file to continue")
		exit()
                
	else:
		print("executing the trace",sys.argv[1])
		filename=sys.argv[1]
        
		
		with open(filename,'r') as f:
			for line in f:
				l=line.split(' ')
				create_inputQ(l)
		datastructure()
		inputprocess()
		#a=l11cache.keys()
		#print(len(a))
	
		
		
		outfile="output.txt"
		with open(outfile, 'a') as s:
			s.write('Executing Trace : %s\n\n'% filename )
			s.write("Simulated Cycles :  %s\n\n" % cycle)
			s.write("L1 cache access: %s\n\n"%l1cacheaccess)
              		
			s.write("L1 cache misses: core wise\n")		
			for key,value in hitmiss.items():
				s.write("core:%s \t hits:%s \t readmiss: %s \t writemiss: %s \t upgrdmiss: %s\n\n"%(key,value[0],value[1],value[2],value[3]))
			
			
			s.write("L2 cache misses:%s\n\n"%l2miss)
			s.write("L1 msg counts core wise\n")
			for key,value in L1msgcount.items():
				s.write("%s:%s\n"%(key,value))
			
			s.write("\n")	
			s.write("L2 msg counts\n\n")
			for key,value in L2msgcount.items():
				s.write("%s:%s \n"%(key,value))
		
			s.write("........................................................................................................................................................\n\n")
		

			

def datastructure():
	global inputQ0,inputQ1,inputQ2,inputQ3,inputQ4,inputQ5,inputQ6,inputQ7,cycle,globalid,L2msgcount,l2miss,OttTable,AckTable
	global l10cache,l11cache,l13cache,l14cache,l15cache,l16cache,l17cache,l12cache,l1cacheaccess,hitmiss,l2cache,L1msgcount,l1miss,l1hits
	global l11msgQ,l12msgQ,l13msgQ,l14msgQ,l15msgQ,l16msgQ,l17msgQ,l10msgQ,l21msgQ,l22msgQ,l23msgQ,l24msgQ,l25msgQ,l26msgQ,l27msgQ,l20msgQ
	hitmiss=dict()
	l2miss=l1hits=0
	l1miss=0
	hitmiss=dict()
	for i in range(0,8):
			hitmiss[i]=[0,0,0,0]
	l1cacheaccess=dict()
	for i in range(0,8):
		l1cacheaccess[i]=0
	l2cacheaccess=0
	l11cache=dict();l12cache=dict();l13cache=dict();l14cache=dict();l15cache=dict();l16cache=dict();l17cache=dict();l10cache=dict();l2cache=dict()	
	l11msgQ=list();l12msgQ=list();l13msgQ=list();l14msgQ=list();l15msgQ=list();l16msgQ=list();l17msgQ=list();l10msgQ=list()
	
	l21msgQ=list();l22msgQ=list();l23msgQ=list();l24msgQ=list();l25msgQ=list();l26msgQ=list();l27msgQ=list();l20msgQ=list()
	AckTable=dict()
	for i in range(0,8):
		AckTable[i]=list()  ###{1:[[request,destination-coreid,source-bankid,blockaddress],[],[]],2:.........}
	
	
	OttTable=dict()
	for i in range(0,8):
		OttTable[i]=list()   #####{1:[[coreid,requestsent,destination,address,state,invalidbit,noofsharers,noofackreceived,[pendingrequest]],[]],2:[]}
	
	L1msgcount=dict()
	L1msgcount['Get']=[0,0,0,0,0,0,0,0];L1msgcount['GetX']=[0,0,0,0,0,0,0,0];L1msgcount['Put']=[0,0,0,0,0,0,0,0];L1msgcount['PutE']=[0,0,0,0,0,0,0,0];
	L1msgcount['PutX']=[0,0,0,0,0,0,0,0];L1msgcount['Inval']=[0,0,0,0,0,0,0,0];L1msgcount['InvalAck']=[0,0,0,0,0,0,0,0];L1msgcount['Nack']=[0,0,0,0,0,0,0,0];
	L1msgcount['WbInval']=[0,0,0,0,0,0,0,0];L1msgcount['WbAck']=[0,0,0,0,0,0,0,0]
	
	L2msgcount=dict()
	L2msgcount['Get']=0;L2msgcount['GetX']=0;L2msgcount['Upgrd']=0;L2msgcount['SWB']=0;L2msgcount['Ack']=0;L2msgcount['WB']=0



def create_inputQ(line):
	global inputQ0,inputQ2,inputQ3,inputQ4,inputQ5,inputQ6,inputQ7,inputQ1
	if int(line[0])==0:
		inputQ0.append([int(line[1]),line[2],int(line[3])])                        # [address , state , globalcount]
	elif int(line[0])==1:
		inputQ1.append([int(line[1]),line[2],int(line[3])])
	elif int(line[0])==2:
		inputQ2.append([int(line[1]),line[2],int(line[3])])
	elif int(line[0])==3:
		inputQ3.append([int(line[1]),line[2],int(line[3])])
	elif int(line[0])==4:
		inputQ4.append([int(line[1]),line[2],int(line[3])])
	elif int(line[0])==5:
		inputQ5.append([int(line[1]),line[2],int(line[3])])
	elif int(line[0])==6:
		inputQ6.append([int(line[1]),line[2],int(line[3])])
	elif int(line[0])==7:
		inputQ7.append([int(line[1]),line[2],int(line[3])])





def inputprocess():
	global cycle,inputQ1,inputQ2,inputQ3,inputQ4,inputQ5,inputQ6,inputQ7,inputQ0,globalid,l11cache,l12cache,l13cache,l14cache,l15cache,l16cache,l17cache,l10cache
	maximum=max([inputQ1[-1][2],inputQ2[-1][2],inputQ3[-1][2],inputQ4[-1][2],inputQ5[-1][2],inputQ6[-1][2],inputQ7[-1][2],inputQ0[-1][2]])
	
	while globalid <= maximum:
		
		cycle+=1	
		if inputQ0:
			if globalid+1==inputQ0[0][2]:
				globalid+=1
				#print(globalid)
				L1cache_find(0,inputQ0[0][0],inputQ0[0][1],l10cache)
				del inputQ0[0]
		if inputQ1:
			if globalid+1==inputQ1[0][2]:
				globalid+=1
				#print(globalid)
				L1cache_find(1,inputQ1[0][0],inputQ1[0][1],l11cache)
				del inputQ1[0]
		if inputQ2:
			if globalid+1==inputQ2[0][2]:
				globalid+=1
				#print(globalid)
				L1cache_find(2,inputQ2[0][0],inputQ2[0][1],l12cache)
				del inputQ2[0]
		if inputQ3:
			if globalid+1==inputQ3[0][2]:
				globalid+=1
				#print(globalid)
				L1cache_find(3,inputQ3[0][0],inputQ3[0][1],l13cache)
				del inputQ3[0]
		if inputQ4:
			if globalid+1==inputQ4[0][2]:
				globalid+=1
				#print(globalid)
				L1cache_find(4,inputQ4[0][0],inputQ4[0][1],l14cache)
				del inputQ4[0]
		if inputQ5:
			if globalid+1==inputQ5[0][2]:
				globalid+=1
				#print(globalid)
				L1cache_find(5,inputQ5[0][0],inputQ5[0][1],l15cache)
				del inputQ5[0]
		if inputQ6:
			if globalid+1==inputQ6[0][2]:
				globalid+=1
				#print(globalid)
				L1cache_find(6,inputQ6[0][0],inputQ6[0][1],l16cache)
				del inputQ6[0]
		if inputQ7:
			if globalid+1==inputQ7[0][2]:
				globalid+=1
				#print(globalid)
				L1cache_find(7,inputQ7[0][0],inputQ7[0][1],l17cache)
				del inputQ7[0]
			
		L1msgQ_process()
		L2msgQ_process()	
		
		if globalid==maximum:
			break
				
	




def L1msgQ_process():
	
	global l11msgQ,l12msgQ,l13msgQ,l14msgQ,l15msgQ,l16msgQ,l17msgQ,l10msgQ,l11cache,l12cache,l13cache,l14cache,l15cache,l16cache,l17cache,l10cache
	
	
	if l11msgQ:
		L1msgs(l11msgQ[0],l11cache)
		del l11msgQ[0]

	if l12msgQ:
		L1msgs(l12msgQ[0],l12cache)
		del l12msgQ[0]
	if l13msgQ:
		L1msgs(l13msgQ[0],l13cache)
		del l13msgQ[0]
	if l14msgQ:
		L1msgs(l14msgQ[0],l14cache)
		del l14msgQ[0]
	if l15msgQ:
		L1msgs(l15msgQ[0],l15cache)
		del l15msgQ[0]
	if l16msgQ:
		L1msgs(l16msgQ[0],l16cache)
		del l16msgQ[0]
	if l17msgQ:
		L1msgs(l17msgQ[0],l17cache)
		del l17msgQ[0]
	if l10msgQ:
		L1msgs(l10msgQ[0],l10cache)
		del l10msgQ[0]



def L1msgs(msg,l1cache):
	global l11msgQ,l12msgQ,l13msgQ,l14msgQ,l15msgQ,l16msgQ,l17msgQ,l10msgQ,l11cache,l12cache,l13cache,l14cache,l15cache,l16cache,l17cache,l10cache,L1msgcount
	
	if msg:
		if msg[0]=='Get':
			LGet(msg,l1cache)
			L1msgcount['Get'][msg[1]]+=1
		elif msg[0]=='GetX':
			LGetX(msg,l1cache)
			L1msgcount['GetX'][msg[1]]+=1
		elif msg[0]=='Put':
			Put(msg,l1cache)
			L1msgcount['Put'][msg[1]]+=1
		elif msg[0]=='PutE':
			PutE(msg,l1cache)
			L1msgcount['PutE'][msg[1]]+=1
		elif msg[0]=='PutX':
			PutX(msg,l1cache)
			L1msgcount['PutX'][msg[1]]+=1
		elif msg[0]=='Inval':
			Inval(msg,l1cache)
			L1msgcount['Inval'][msg[1]]+=1
		elif msg[0]=='InvalAck':
			InvalAck(msg,l1cache)
			L1msgcount['InvalAck'][msg[1]]+=1
		elif msg[0]=='Nack':
			Nack(msg,l1cache)
			L1msgcount['Nack'][msg[1]]+=1
		elif msg[0]=='WbInval':
			WbInval(msg,l1cache)
			L1msgcount['WbInval'][msg[1]]+=1
		elif msg[0]=='WbAck':
			WbAck(msg,l1cache)
			L1msgcount['WbAck'][msg[1]]+=1	
			




def L2msgQ_process():
	global l21msgQ,l22msgQ,l23msgQ,l24msgQ,l25msgQ,l26msgQ,l27msgQ,l20msgQ
	
	if l21msgQ:
		L2msgs(l21msgQ[0])
		del l21msgQ[0]
	if l22msgQ:
		L2msgs(l22msgQ[0])
		del l22msgQ[0]

	if l23msgQ:
		L2msgs(l23msgQ[0])
		del l23msgQ[0]
	if l24msgQ:
		L2msgs(l24msgQ[0])
		del l24msgQ[0]
	if l25msgQ:
		L2msgs(l25msgQ[0])
		del l25msgQ[0]
	if l26msgQ:
		L2msgs(l26msgQ[0])
		del l26msgQ[0]
	if l27msgQ:
		L2msgs(l27msgQ[0])
		del l27msgQ[0]
	if l20msgQ:
		L2msgs(l20msgQ[0])
		del l20msgQ[0]



def L2msgs(msg):
	global L2msgcount
	if msg:
		if msg[0]=='Get':
			Get(msg)
			L2msgcount['Get']+=1
		elif msg[0]=='GetX':
			GetX(msg)
			L2msgcount['GetX']+=1
		elif msg[0]=='Upgrd':
			Upgrd(msg)
			L2msgcount['Upgrd']+=1
		elif msg[0]=='SWB':
			SWB(msg)
			L2msgcount['SWB']+=1
		elif msg[0]=='Ack':
			Ack(msg)
			L2msgcount['Ack']+=1
		if msg[0]=='WB':
			WB(msg)
			L2msgcount['WB']+=1
		
	



def L1cache_find(coreid,address,action,Lcache): #(coreid,address,R/W,Lcache)
	global l11msgQ,l12msgQ,l13msgQ,l14msgQ,l15msgQ,l16msgQ,l17msgQ,l10msgQ,l11cache,l12cache,l13cache,l14cache,l15cache,l16cache,l17cache,l10cache,l1miss,l1hits
	
	global l1cacheaccess,hitmiss
	
	binaddr=bin(address)[2:].zfill(64)
	
	l1cacheaccess[coreid]+=1
	
	tag=binaddr[0:52]
	
	setindex=binaddr[52:58]
	
	temp=[]
	
	blockscount=0
	
	hits=readmiss=writemiss=upgrdmiss=0
	
	if setindex in Lcache.keys():
		
		for i in range(0,len(Lcache[setindex])):
			
			if Lcache[setindex][i][0]==tag:
				blockscount-=1
				temp=Lcache[setindex][i]
				if  temp[1]=='M'  and action=='W':
					hits+=1
					Lcache[setindex].remove(temp)
					Lcache[setindex].insert(0,temp)					
				
				elif (temp[1]=='M' or temp[1]=='S' or temp[1]=='E')  and action=='R':
					hits+=1
					Lcache[setindex].remove(temp)
					Lcache[setindex].insert(0,temp)
				
				elif temp[1]=='E' and action=='W':
					hits+=1
					
					Lcache[setindex].remove(temp)
					Lcache[setindex].insert(0,[tag,'M'])
					
				elif temp[1]=='S' and action=='W':
					upgrdmiss+=1
					Lcache[setindex].remove(temp)
					OttTable_Structure([coreid,address,'Upgrd',0,0,0,0])
					
				break
			else:
				blockscount+=1
				
		if blockscount==len(Lcache[setindex]):
			if action=='R':
				readmiss+=1
				OttTable_Structure([coreid,address,'Get',0,0,0,0])
			elif action=='W':
				writemiss+=1 
				OttTable_Structure([coreid,address,'GetX',0,0,0,0])
	else:
		
		Lcache[setindex]=list()
		if action=='R':
			readmiss+=1
			OttTable_Structure([coreid,address,'Get',0,0,0,0])
		elif action=='W':
			writemiss+=1 
			OttTable_Structure([coreid,address,'GetX',0,0,0,0])
		
	hitmiss[coreid]=[hitmiss[coreid][0]+hits,hitmiss[coreid][1]+readmiss,hitmiss[coreid][2]+writemiss,hitmiss[coreid][3]+upgrdmiss]				 


def OttTable_Structure(mesg):		#[coreid,address,Upgrd,inavlidbit,noof sharerscount,invalackcountrecv,pendingW]
	
	global OttTable,hitmiss,l1hits,l1miss	
	
	coreid=mesg[0]
	address=mesg[1]
	binadr=bin(mesg[1])[2:].zfill(64)
	hits=readmiss=writemiss=upgrdmiss=0
	bankid=binadr[55:58]
	request=mesg[2]
	pending=mesg[6]
	hit=readmiss=writemiss=upgrdmiss=0
	itemcount=0
	
	for i in range(0,len(OttTable[coreid])):
		
		if OttTable[coreid][i][1]==address:
				itemcount-=1
			
				if request=='Get':
			 		hits+=1
			 		readmiss-=1
			 
				elif  request=='GetX':
					hits+=1
					writemiss-=1
					if OttTable[coreid][i][2]=='Get':
						OttTable[coreid][i][6]=1
				elif  request=='Upgrd':
					hits+=1
					upgrdmiss-=1
					if OttTable[coreid][i][2]=='Get':
						OttTable[coreid][i][6]=1
					
				break
		else:
			itemcount+=1
				
	if itemcount==len(OttTable[coreid]): # if address not in table
		
		OttTable[coreid].append(mesg)
		
		if request=='Get':
			Message(['Get',bankid,coreid,mesg[1]])
		
		elif request=='GetX':
			Message(['GetX',bankid,coreid,mesg[1]])
		
		elif request=='Upgrd':
			Message(['Upgrd',bankid,coreid,mesg[1]])
	
	hitmiss[coreid]=[hitmiss[coreid][0]+hits,hitmiss[coreid][1]+readmiss,hitmiss[coreid][2]+writemiss,hitmiss[coreid][3]+upgrdmiss]


def Message(message): 
	
	global l11msgQ,l12msgQ,l13msgQ,l14msgQ,l15msgQ,l16msgQ,l17msgQ,l10msgQ,l21msgQ,l22msgQ,l23msgQ,l24msgQ,l25msgQ,l26msgQ,l27msgQ,l20msgQ
	
	if message[1]=='000':
		l20msgQ.append(message)
	elif message[1]=='001':
		l21msgQ.append(message)
	elif message[1]=='010':
		l22msgQ.append(message)
	elif message[1]=='011':
		l23msgQ.append(message)
	elif message[1]=='100':
		l24msgQ.append(message)
	elif message[1]=='101':
		l25msgQ.append(message)
	elif message[1]=='110':
		l26msgQ.append(message)
	elif message[1]=='111':
		l27msgQ.append(message)
	elif int(message[1])==0:
		l10msgQ.append(message)
	elif int(message[1])==1:
		l11msgQ.append(message)
	elif int(message[1])==2:
		l12msgQ.append(message)
	elif int(message[1])==3:
		l13msgQ.append(message)
	elif int(message[1])==4:
		l14msgQ.append(message)
	elif int(message[1])==5:
		l15msgQ.append(message)
	elif int(message[1])==6:
		l16msgQ.append(message)
	elif int(message[1])==7:
		l17msgQ.append(message)


#def Nack_Table():
#	pass

#def Ack_Buffer():
#	pass

#def L1_insert(coreid,address,state,l1cache):
#	binadr=bin(address)[2:].zfill(32)
#	pass



################################################### HERE IN INSERT SEE HOW TO RESOLVE THE CASE OF WB -> REQUEST COMES BEFORE THE WB REACHES

def L1_insert(coreid,address,state,l1cache):
	global l11msgQ,l12msgQ,l13msgQ,l14msgQ,l15msgQ,l16msgQ,l17msgQ,l10msgQ,l11cache,l12cache,l13cache,l14cache,l15cache,l16cache,l17cache,l10cache
	
	binadr=bin(address)[2:].zfill(64)
	tag=binadr[0:52]
	index=binadr[52:58]
	blockscounts=0
	if index in l1cache.keys():
		if len(l1cache[index])<8:
			l1cache[index].insert(0,[tag,state])
		else:
			evictedblock=l1cache[index].pop()
			if (evictedblock[1]=='M' or evictedblock[1]=='E') :
				Message(['WB',binadr[55:58],coreid,address])
			l1cache[index].insert(0,[tag,state])
	else:
		l1cache[index]=list()
		l1cache[index].append([tag,state])
		






############################################################################################ L1 Msgs ##################################################################################################
## Messages [request,destination,source,address]
#Get,GetX [request,dest(bid/coreid),src(req cid),address]
#upgrd [request,dest(bid),src(coreid),address]
#Put,PutE[request,destination(coreid),address]
#PutX[request,destination(coreid),address,Invalidbit,no.of sharers]
#SWB [request,dest(Bid),source(coreid),address]
#Inval [request,dest(coreid with S ),source(requestor coreid),address]
#InvalAck [request/ack,dest(coreid)[requestor ],src[which is sending the ack],address]
#Nack [request,dest(coreid),source(bid),address]
#WB [request,dest(Bid),src(coreid),address]
#WBAck [request,dest(coreid),src(bid),address]
#Ack [request,dest(bid),src(coreid),address]
#WInval[ request,dest(cid),address]



#Get[request,dest(coreid),src(req cid),address]
def LGet(msg,l1cache):
	##THIS IS BECOZ , THIS IS THE CURRENT OWNER, S0 CHECK IN CACHE IF ITS THERE , DEMOTE TO S STATE , PUT , SWB;ELSE CHECK IN OTT TABLE
	### IF INVALID BIT = = 1  AND NOOFSHARERS != ACKS RECV , PUT THE MSG IN ACK TABLE 
	global l11msgQ,l12msgQ,l13msgQ,l14msgQ,l15msgQ,l16msgQ,l17msgQ,l10msgQ,l11cache,l12cache,l13cache,l14cache,l15cache,l16cache,l17cache,l10cache
	
	global OttTable,AckTable
	request=msg[0]
	selfcoreid=msg[1]
	destcoreid=msg[2]
	address=msg[3]
	binadr=bin(address)[2:].zfill(64)
	tag=binadr[0:52]
	index=binadr[52:58]
	itemcount=0
	ottitemcount=0
	if index in l1cache.keys():
		for i in range(0,len(l1cache[index])):
			if l1cache[index][i][0]==tag:
				itemcount-=1
				l1cache[index][i][1]='S'
				temp=l1cache[index][i]
				l1cache[index].remove(temp)
				l1cache[index].insert(0,temp)
				
				Message(['Put',destcoreid,address])
				Message(['SWB',binadr[55:58],selfcoreid,address])
				break
			else:
				itemcount+=1
		if itemcount==len(l1cache[index]):
			for j in range(0,len(OttTable[selfcoreid])):
				if OttTable[selfcoreid][j][1]==address:
					ottitemcount-=1
					if OttTable[selfcoreid][j][3]==1: 
					# AckTable {coreid:[['Request-type','Coreid',Destination(Requested Coreid), Address],[],..],..}
	
						AckTable[selfcoreid].append(msg)
					else:
						pass#print("some error in Lget not recieved the invalidbit")		 

#######################################################################################################################
#GetX [request,dest(coreid),src(req cid),address]
def LGetX(msg,l1cache):
	##IF PRESENT IN CACHE, PUTX, REMOVE , ACK 
	## ELSE CHECK IN OTT , IF INVALIDBIT==1 AND NO OF SHARERS!= , PUT IN ACK TABLE
	global l11msgQ,l12msgQ,l13msgQ,l14msgQ,l15msgQ,l16msgQ,l17msgQ,l10msgQ,l11cache,l12cache,l13cache,l14cache,l15cache,l16cache,l17cache,l10cache
	global OttTable,AckTable
	request=msg[0]
	selfcoreid=msg[1]
	destcoreid=msg[2]
	address=msg[3]
	binadr=bin(address)[2:].zfill(64)
	tag=binadr[0:52]
	index=binadr[52:58]
	itemcount=0
	ottitemcount=0
	if index in l1cache.keys():
		for i in range(0,len(l1cache[index])):
			if l1cache[index][i][0]==tag:
				itemcount-=1
				l1cache[index].remove(l1cache[index][i])
				
				
				Message(['PutX',destcoreid,address,0,0])
				Message(['Ack',binadr[55:58],selfcoreid,address])
				break
			else:
				itemcount+=1
		if itemcount==len(l1cache[index]):
			for j in range(0,len(OttTable[selfcoreid])):
				if OttTable[selfcoreid][j][1]==address:
					ottitemcount-=1
					if OttTable[selfcoreid][j][3]==1: 
					# AckTable {coreid:[['Request-type','Coreid',Destination(Requested Coreid), Address],[],..],..}
	
						AckTable[selfcoreid].append(msg)
					else:
						pass#print("some error in LgetX not recieved the invalidbit")		 






















########################################################################################################################
#OttTable[coreid,address,Upgrd,inavlidbit,noof sharerscount,invalackcountrecv,pendingW]
#Put[request,destination(coreid),address]
def Put(msg,l1cache):
	global l11msgQ,l12msgQ,l13msgQ,l14msgQ,l15msgQ,l16msgQ,l17msgQ,l10msgQ,l11cache,l12cache,l13cache,l14cache,l15cache,l16cache,l17cache,l10cache
	global OttTable	
	request=msg[0]
	coreid=msg[1]
	address=msg[2]
	binadr=bin(address)[2:].zfill(64)
	itemcount=0
	temp=[]
	for i in range(0,len(OttTable[coreid])):
		if OttTable[coreid][i][1]==address:
			itemcount-=1
			temp=OttTable[coreid][i]
			if temp[2]=='Get':
				if temp[6]==0: #no writes or upgrades pending
					L1_insert(coreid,address,'S',l1cache)
					OttTable[coreid].remove(temp)
				
				elif temp[6]==1: #pending bit is present
					OttTable[coreid][i][2]='GetX'	
					OttTable[coreid][i][6]=0
					Message(['Upgrd',binadr[55:58],coreid,address]) # look at this GetX or Upgrd??
				 	
				break
			else:
				pass#print("Ott table entry missing in Put")	
		else:
			itemcount+=1
	if itemcount==len(OttTable[coreid]):
		pass#print("some error in Put")

#############################################################################################################################

#PutX[request,destination(coreid),address,Invalidbit,no.of sharers]
def PutX(msg,l1cache):
	global l11msgQ,l12msgQ,l13msgQ,l14msgQ,l15msgQ,l16msgQ,l17msgQ,l10msgQ,l11cache,l12cache,l13cache,l14cache,l15cache,l16cache,l17cache,l10cache
	global OttTable
	request=msg[0]
	coreid=msg[1]
	address=msg[2]
	invalidbit=msg[3]
	noofsharers=msg[4]
	itemcount=0
	for i in range(0,len(OttTable[coreid])):
		if OttTable[coreid][i][1]==address:
			itemcount-=1
			if invalidbit==0:
				L1_insert(coreid,address,'M',l1cache)
				OttTable[coreid].remove(OttTable[coreid][i])
			elif invalidbit==1:
				OttTable[coreid][i][3]=1
				OttTable[coreid][i][4]=noofsharers
			break
		else:
			itemcount+=1
	if itemcount==len(OttTable[coreid]):
		pass#print("some error in PutX")
		
#################################################################################################################################
#PutE[request,destination(coreid),address]
def PutE(msg,l1cache):
	global l11msgQ,l12msgQ,l13msgQ,l14msgQ,l15msgQ,l16msgQ,l17msgQ,l10msgQ,l11cache,l12cache,l13cache,l14cache,l15cache,l16cache,l17cache,l10cache
	global OttTable
	request=msg[0]
	coreid=msg[1]
	address=msg[2]
	temp=[]
	itemcount=0
	for i in range(0,len(OttTable[coreid])):
		if OttTable[coreid][i][1]==address:
			itemcount-=1
			temp=OttTable[coreid][i]
			if temp[2]=='Get':
				if temp[6]==0:
					L1_insert(coreid,address,'E',l1cache)
					OttTable[coreid].remove(temp)
				elif temp[6]==1:
					L1_insert(coreid,address,'M',l1cache)
					OttTable[coreid].remove(temp)
				break
			else:
				pass#print("Ott table entry missing in PutE")
				
		else:
			itemcount+=1
	if itemcount==len(OttTable[coreid]):
		pass#print("some error in PutE")

#################################################################################################################################


#Inval [request,dest(coreid with S ),source(requestor coreid),address]
def Inval(msg,l1cache):
	global l11msgQ,l12msgQ,l13msgQ,l14msgQ,l15msgQ,l16msgQ,l17msgQ,l10msgQ,l11cache,l12cache,l13cache,l14cache,l15cache,l16cache,l17cache,l10cache
	
	request=msg[0]
	selfcoreid=msg[1]
	destcoreid=msg[2]
	address=msg[3]
	binadr=bin(address)[2:].zfill(64)
	tag=binadr[0:52]
	index=binadr[52:58]
	itemcount=0
	if index in l1cache.keys():
		for i in range(0,len(l1cache[index])):
			if l1cache[index][i][0]==tag:
				itemcount-=1
				Message(['InvalAck',destcoreid,selfcoreid,address])
				l1cache[index].remove(l1cache[index][i])
				break
			else:
				itemcount+=1
		if itemcount==len(l1cache[index]):
			Message(['InvalAck',destcoreid,selfcoreid,address])
					
#################################################################################################################################

#### TAKE CARE WHILE SENDING INVAL , DONT SEND TO THE SELF BLOCK BECOZ IN UPGRD IT ALSO WAS IN S ################################	

#OttTable[coreid,address,Upgrd,inavlidbit,noof sharerscount,invalackcountrecv,pendingW]
#InvalAck [request/ack,dest(coreid)[requestor ],src[which is sending the ack],address]
def InvalAck(msg,l1cache):
	global OttTable,AckTable
	global l11msgQ,l12msgQ,l13msgQ,l14msgQ,l15msgQ,l16msgQ,l17msgQ,l10msgQ,l11cache,l12cache,l13cache,l14cache,l15cache,l16cache,l17cache,l10cache
	
	request=msg[0]
	coreid=msg[1]
	address=msg[3]
	binadr=bin(address)[2:].zfill(64)
	itemcount=0
	temp=[]
	ackitemcount=0
	#CHECK OTT FOR INVAL BIT, INCREMENT ACK , CHECK SHARERS==NOOFACK:IF YES  :CHECK ACK BUFFER, IF NO INSERT AS M , IF ACK BUFFER YES ->CHECK-> GET-INSERT IN S STATE, PUT , SWB;
	# IF GETX-PUTX,SEND ACK NO INSERT;
	for i in range(0,len(OttTable[coreid])):
		if OttTable[coreid][i][1]==address:
			itemcount-=1
			if OttTable[coreid][i][3]==1:
				OttTable[coreid][i][5]+=1
				if OttTable[coreid][i][4]==OttTable[coreid][i][5]:
					for j in range(0,len(AckTable[coreid])):
						if AckTable[coreid][j][3]==address:
							ackitemcount-=1
							if AckTable[coreid][j][0]=='Get':
								L1_insert(coreid,address,'S',l1cache)
								Message(['Put',AckTable[coreid][j][1],address])
								Message(['SWB',binadr[55:58],coreid,address])			
								
								
							elif AckTable[coreid][j][0]=='GetX':
								Message(['PutX',AckTable[coreid][j][1],address,0,0])
								Message(['Ack',binadr[55:58],coreid,address])		
						else:
							ackitemcount+=1
					if ackitemcount==len(AckTable[coreid]):
						L1_insert(coreid,address,'M',l1cache)
				OttTable[coreid].remove(OttTable[coreid][i])
			break
				
				
		else:
			itemcount+=1
	if itemcount==len(OttTable[coreid]):
		pass#print("some error in InvalAck")	
	
	# AckTable {coreid:[['Request-type','Coreid',Destination(Requested Coreid), Address],[],..],..}
	
	

###################################################################################################################################
#Nack [request,dest(coreid),source(bid),address,requested-msg] ##JUST REMOVE FROM OTT IF U WANT INSERT IT IN HEAD OF I/P QUEUE 


# for now removed it from Ott table
def Nack(msg,l1cache):
	global l11msgQ,l12msgQ,l13msgQ,l14msgQ,l15msgQ,l16msgQ,l17msgQ,l10msgQ,l11cache,l12cache,l13cache,l14cache,l15cache,l16cache,l17cache,l10cache
	global OttTable,hitmiss
	request=msg[0]
	coreid=msg[1]
	bankid=msg[2]
	address=msg[3]
	request_type=msg[4]
	itemcount=0
	for i in range(0,len(OttTable[coreid])):
		if OttTable[coreid][i][1]==address:
			itemcount-=1
			if request_type=='Get':
				hitmiss[coreid][1]-=1
			elif request_type=='GetX':
				hitmiss[coreid][2]-=1
			elif request_type=='Upgrd':
				hitmiss[coreid][3]-=1
			hitmiss[coreid][0]+=1
			OttTable[coreid].remove(OttTable[coreid][i])
			
			break
		else:
			itemcount+=1
	if itemcount==len(OttTable[coreid]):
		pass#print("some issue with Nack not being found in ott")

####################################################################################################################################
#WInval[ request,dest(cid),address]
def WbInval(msg,l1cache):
	global l11msgQ,l12msgQ,l13msgQ,l14msgQ,l15msgQ,l16msgQ,l17msgQ,l10msgQ,l11cache,l12cache,l13cache,l14cache,l15cache,l16cache,l17cache,l10cache
	
	request=msg[0]
	coreid=msg[1]
	address=msg[2]
	#binadr=bin(address)[2:].zfill(64)
	tag=address[0:52]
	index=address[52:58]
	if index in l1cache.keys():
		for i in range(0,len(l1cache[index])):
			if l1cache[index][i][0]==tag:
				l1cache[index].remove(l1cache[index][i])
				break
#IF THE BLOCK IS IN S OR E STATE LEAVE , IF ITS IN M STATE , ALSO JUST REMOVE , WHILE SENDING ONLY 


#####################################################################################################################################
#WBAck [request,dest(coreid),src(bid),address]
def WbAck(msg,l1cache):
	coreid=msg[1]
	###Just count the WbAcks



###################################################################################################### L2 Msgs ########################################################################################

#Get,GetX [request,dest(bid/coreid),src(req cid),address]
#upgrd [request,dest(bid),src(coreid),address]
#Put,PutE[request,destination(coreid),address]
#PutX[request,destination(coreid),address,Invalidbit,no.of sharers]
#SWB [request,dest(Bid),source(coreid),address]
#Inval [request,dest(coreid with S ),source(requestor coreid),address]
#InvalAck [request/ack,dest(coreid)[requestor ],src[which is sending the ack],address]
#Nack [request,dest(coreid),source(bid),address]
#WB [request,dest(Bid),src(coreid),address]
#WBAck [request,dest(coreid),src(bid),address]
#Ack [request,dest(bid),src(coreid),address]
#WInval[ request,dest(cid),address]


#Get,GetX [request,bid,src(req cid),address]
#upgrd [request,dest(bid),src(coreid),address]

def Get(msg):
	global l2cache,l2miss
	request=msg[0]
	bankid=msg[1]
	coreid=msg[2]
	address=msg[3]	
	binadr=bin(address)[2:].zfill(64)
	tag=binadr[0:46]
	index=binadr[46:58]
	itemcount=0
	temp=[]
	if index in l2cache.keys():
		for i in range(0,len(l2cache[index])):
			if l2cache[index][i][3]==tag:
				itemcount-=1
				temp=l2cache[index][i]
				if temp[0]==1:
					Message(['Nack',coreid,bankid,address,request])
				elif temp[0]==0:
					if temp[1]==0:
						if 'S' in temp[2]:
							Message(['Put',coreid,address])
							l2cache[index][i][2][coreid]='S'
							temp=l2cache[index][i]
							l2cache[index].remove(temp)
							l2cache[index].insert(0,temp)
						elif ('S' not in temp[2]) and ('M' not in temp[2]):
							Message(['PutE',coreid,address])
							l2cache[index][i][2][coreid]='M'
							l2cache[index][i][1]=1
							temp=l2cache[index][i]
							l2cache[index].remove(temp)
							l2cache[index].insert(0,temp)
						break
					elif temp[1]==1:
						if 'M' in temp[2]:
							ownercore=temp[2].index('M')
							Message(['Get',ownercore,coreid,address])
							l2cache[index][i][0]=1
							l2cache[index][i][2][coreid]='S'
							temp=l2cache[index][i]
							l2cache[index].remove(temp)
							l2cache[index].insert(0,temp)
						break
				
				#IF PENDING BIT IS OFF , DIRTY BIT IS OFF -> CHECK FOR OTHER S PRESENT , IF YES PUT , S STATE, ELSE I.E NO S NOR M PUTE STATE
				# IF DIRTY BIT IS ON , CHECK FOR M BIT , SEND THE REQUEST AS GET TO OWNER CORE i.e. M BITS INDEX , PUT 1 FOR THE PENDING BIT , S FOR MYSELF
				# IF PENDING BIT IS ON , SEND A  NACK BACK  
			else:
				itemcount+=1 # IF BLOCK NOT FOUND INSERT THE BLOCK IN M STATE, PUTE
			if itemcount==len(l2cache[index]):
				directory=['I','I','I','I','I','I','I','I']
				directory[coreid]='M'
				Message(['PutE',coreid,address])
				l2miss+=1
				L2_insert([0,1,directory,address])
	else:
		directory=['I','I','I','I','I','I','I','I']
		directory[coreid]='M'
		Message(['PutE',coreid,address])
		l2miss+=1		
		L2_insert([0,1,directory,address])
		#L2_insert() # IF BLOCK NOT FOUND INSERT THE BLOCK IN M STATE, PUTE
		
#######################################################################################################################################################################
def GetX(msg):
	
	#IF PENDING BIT IS OFF , DIRTY BIT IS OFF -> CHECK FOR OTHER S PRESENT , SEND INVAL , M STATE , PUTX
	# IF DIRTY BIT IS ON , CHECK FOR M BIT , SEND THE REQUEST AS GETX TO OWNER CORE i.e. M BITS INDEX , PUT 1 FOR THE PENDING BIT , WAIT FOR ACK
	# IF PENDING BIT IS ON , SEND A  NACK BACK
	global l2cache,l2miss
	request=msg[0]
	bankid=msg[1]
	coreid=msg[2]
	address=msg[3]	
	binadr=bin(address)[2:].zfill(64)
	tag=binadr[0:46]
	index=binadr[46:58]
	itemcount=0
	temp=[]
	count=0
	if index in l2cache.keys():
		for i in range(0,len(l2cache[index])):
			if l2cache[index][i][3]==tag:
				itemcount-=1
				temp=l2cache[index][i]
				if temp[0]==1:
					Message(['Nack',coreid,bankid,address,request])
				elif temp[0]==0:
					if temp[1]==0:
						if 'S' in temp[2]:
							for a in temp[2]:
								if a=='S':
									destcore=temp[2].index(a)
									Message(['Inval',destcore,coreid,address])
									count+=1								
							l2cache[index][i][2][coreid]='M'
							l2cache[index][i][1]=1
							
							
							Message(['PutX',coreid,address,1,count])
							temp=l2cache[index][i]
							l2cache[index].remove(temp)
							l2cache[index].insert(0,temp)
						else:
							pass#print("some error in getx")
						break
					elif temp[1]==1:
						if 'M' in temp[2]:
							ownercore=temp[2].index('M')
							Message(['GetX',ownercore,coreid,address])
							l2cache[index][i][0]=1
							l2cache[index][i][2][coreid]='M'
							l2cache[index][i][2][ownercore]='I' 
							temp=l2cache[index][i]
							l2cache[index].remove(temp)
							l2cache[index].insert(0,temp)
						break
				  
			else:
				itemcount+=1 # IF BLOCK NOT FOUND INSERT THE BLOCK IN M STATE, PUTE
			if itemcount==len(l2cache[index]):
				directory=['I','I','I','I','I','I','I','I']
				directory[coreid]='M'
				Message(['PutX',coreid,address,0,0])
				l2miss+=1
				L2_insert([0,1,directory,address])
	else:
		directory=['I','I','I','I','I','I','I','I']
		directory[coreid]='M'
		Message(['PutX',coreid,address,0,0])
		l2miss+=1		
		L2_insert([0,1,directory,address])
		
###########################################################################################################################################################################
def Upgrd(msg):
	#IF PENDING BIT IS OFF , DIRTY BIT IS OFF -> M STATE THEN CHECK FOR OTHER S PRESENT , SEND INVAL , , PUTX
	# IF DIRTY BIT IS ON , CHECK FOR M BIT , SEND THE REQUEST AS GETX TO OWNER CORE i.e. M BITS INDEX , PUT 1 FOR THE PENDING BIT , WAIT FOR ACK
	# IF PENDING BIT IS ON , SEND A  NACK BACK
	global l2cache,l2miss
	request=msg[0]
	bankid=msg[1]
	coreid=msg[2]
	address=msg[3]	
	binadr=bin(address)[2:].zfill(64)
	tag=binadr[0:46]
	index=binadr[46:58]
	itemcount=0
	temp=[]
	count=0
	a=''
	if index in l2cache.keys():
		for i in range(0,len(l2cache[index])):
			if l2cache[index][i][3]==tag:
				itemcount-=1
				temp=l2cache[index][i]
				if temp[0]==1:
					Message(['Nack',coreid,bankid,address,request])
				elif temp[0]==0:
					if temp[1]==0:
						l2cache[index][i][2][coreid]='M'
						if 'S' in temp[2]:
							for a in temp[2]:
								if a=='S':
									destcore=temp[2].index(a)
									Message(['Inval',destcore,coreid,address])
									count+=1								
							
							if count>0:
							
								Message(['PutX',coreid,address,1,count])
							elif count==0:
								Message(['PutX',coreid,address,0,count])
							temp=l2cache[index][i]
							l2cache[index].remove(temp)
							l2cache[index].insert(0,temp)
						###CHECK FOR SOME CASE IF OTHER STATES ARE THERE
						break
					elif temp[1]==1:
						if 'M' in temp[2]:
							ownercore=temp[2].index('M')
							Message(['GetX',ownercore,coreid,address])
							l2cache[index][i][0]=1
							l2cache[index][i][2][coreid]='M'
							l2cache[index][i][2][ownercore]='I'
							temp=l2cache[index][i]
							l2cache[index].remove(temp)
							l2cache[index].insert(0,temp)
						break
				  
			else:
				itemcount+=1 # IF BLOCK NOT FOUND INSERT THE BLOCK IN M STATE, PUTE
			
			if itemcount==len(l2cache[index]):
				directory=['I','I','I','I','I','I','I','I']
				directory[coreid]='M'
				Message(['PutX',coreid,address,0,0])
				l2miss+=1
				L2_insert([0,1,directory,address])
	else:
		l2miss+=1
		
		#print("some error index not found")

#SWB [request,dest(Bid),source(coreid),address]
#Inval [request,dest(coreid with S ),source(requestor coreid),address]
#InvalAck [request/ack,dest(coreid)[requestor ],src[which is sending the ack],address]
#Nack [request,dest(coreid),source(bid),address]

#WBAck [request,dest(coreid),src(bid),address]
#Ack [request,dest(bid),src(coreid),address]
#WInval[ request,dest(cid),address]
	
def SWB(msg):
	# CHECK COREID==INDEX OF M  STATE, PENDING BIT=1, PUT S, PENDING BIT TO 0,DIRTY BIT TO0
	global l2cache,l2miss
	request=msg[0]
	bankid=msg[1]
	coreid=msg[2]
	address=msg[3]
	binadr=bin(address)[2:].zfill(64)
	tag=binadr[0:46]
	index=binadr[46:58]
	itemcount=0
	temp=[]
	if index in l2cache.keys():
		for i in range(0,len(l2cache[index])):
			if l2cache[index][i][3]==tag:
				itemcount-=1
				if l2cache[index][i][0]==1:
					if l2cache[index][i][2][coreid]=='M':
						l2cache[index][i][2][coreid]='S'
						l2cache[index][i][0]=0
						l2cache[index][i][1]=0		
						temp=l2cache[index][i]
						l2cache[index].remove(temp)
						l2cache[index].insert(0,temp)
				break	
			else:
			 itemcount+=1
		if itemcount==len(l2cache[index]):
			l2miss+=1	
	else:
		l2miss+=1

def Ack(msg):
	# CHECK IF COREID HAS I STATE AND ALSO THERE IS AN M STATE, PENDING BIT TO 0, DIRTY BIT TO1
	global l2cache,l2miss
	request=msg[0]
	bankid=msg[1]
	coreid=msg[2]
	address=msg[3]
	binadr=bin(address)[2:].zfill(64)
	tag=binadr[0:46]
	index=binadr[46:58]
	itemcount=0
	temp=[]
	if index in l2cache.keys():
		for i in range(0,len(l2cache[index])):
			if l2cache[index][i][3]==tag:
				itemcount-=1
				if l2cache[index][i][0]==1:
					if l2cache[index][i][2][coreid]=='I' and ('M' in l2cache[index][i][2]):
						
						l2cache[index][i][0]=0
						l2cache[index][i][1]=1		
						temp=l2cache[index][i]
						l2cache[index].remove(temp)
						l2cache[index].insert(0,temp)
				break
				
			else:
				itemcount+=1	
		if itemcount==len(l2cache[index]):
			l2miss+=1	
	else:
		l2miss+=1


#WB [request,dest(Bid),src(coreid),address]	
def WB(msg):
	# IF PENDING BIT =0 , DIRECTORY[INDEX]=I-> IF NO M OR S REMOVE , IF NO M , PUT DIRTY BIT TO 0
	#IF PENDING BIT =1 , DIRECTORY ENTRY[INDEX][M]==COREID, SEND A PUT REPLY TO S STATE INDEX IN DIRECTORY, CHANGE M TO S , PENDING TO 0, DIRTY TO 0
	#IF PENDING BIT =1 , DIRECTORY ENTRY[INDEX][I]==COREID, SEND A PUTX REPLY TO M STATE INDEX IN DIRECTORY, PENDING TO 0, DIRTY TO 1
	global l2cache,l2miss
	request=msg[0]
	bankid=msg[1]
	coreid=msg[2]
	address=msg[3]
	binadr=bin(address)[2:].zfill(64)
	tag=binadr[0:46]
	index=binadr[46:58]
	itemcount=0
	temp=[]
	if index in l2cache.keys():
		for i in range(0,len(l2cache[index])):
			if l2cache[index][i][3]==tag:
				itemcount-=1
				if l2cache[index][i][0]==0:
					Message(['WbAck',coreid,bankid,address])
					l2cache[index][i][2][coreid]='I'
					if ('S' not in l2cache[index][i][2]) and ('M' not in l2cache[index][i][2]):
						l2cache[index].remove(l2cache[index][i])
					elif 'M' not in l2cache[index][i][2]:
						l2cache[index][i][1]=0
						temp=l2cache[index][i]
						l2cache[index].remove(temp)
						l2cache[index].insert(0,temp)
				
				elif l2cache[index][i][0]==1:
				
					if l2cache[index][i][2][coreid]=='M':
						if 'S' in l2cache[index][i][2]:
							ownercore=l2cache[index][i][2].index('S')
							Message(['Put',ownercore,address])
							l2cache[index][i][2][coreid]='I'
							l2cache[index][i][0]=0
							l2cache[index][i][1]=0
							temp=l2cache[index][i]
							Message(['WbAck',coreid,bankid,address])
							l2cache[index].remove(temp)
							l2cache[index].insert(0,temp)
					elif l2cache[index][i][2][coreid]=='I':
						if 'M' in l2cache[index][i][2]:
							ownercore=l2cache[index][i][2].index('M')
							Message(['PutX',ownercore,address,0,0])
							l2cache[index][i][0]=0
							l2cache[index][i][1]=1
							Message(['WbAck',coreid,bankid,address])
							temp=l2cache[index][i]
							l2cache[index].remove(temp)
							l2cache[index].insert(0,temp)
				break
	else:
		pass
		#l2miss+=1

#######################################################################################################################################################################################################


def L2_insert(addrblock): #[pendingbit,dirtybit,[directory],address]
	global l2cache,l2miss
	address=bin(addrblock[3])[2:].zfill(64)
	tag=address[0:46]
	index=address[46:58]
	#print(addrblock)
	if index in l2cache.keys():
		
		if len(l2cache[index])<16:
			#l2miss+=1
			l2cache[index].insert(0,[addrblock[0],addrblock[1],addrblock[2],tag])
		else:
			evictedblock=l2cache[index].pop()
			for i in range(0,8):
				if evictedblock[2][i]=='S' or evictedblock[2][i]=='M':
					evictedaddress=evictedblock[3]+index
					#print(len(evictedaddress))
					Message(['WbInval',i,evictedaddress])
			l2miss+=1
			l2cache[index].insert(0,[addrblock[0],addrblock[1],addrblock[2],tag])
	else:
		
		#l2miss+=1
		l2cache[index]=list()
		l2cache[index].append([addrblock[0],addrblock[1],addrblock[2],tag])
		
	

#CHECK FOR THE CRCT CORE NUMBERS AND FLOW 
#REMEMBER COREID STARTS FROM 0 

if __name__ == "__main__":
    main()

