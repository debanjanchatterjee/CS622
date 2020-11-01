import time
import sys

memblk=dict()
mb=0
def profshare(tid,address):
	global memblk,mb
	if address in memblk.keys():
		memblk[address].add(tid)
	else:
		memblk[address]=set()
		memblk[address].add(tid)
		mb+=1
pass

def main():
            global memblk,mb
            if len(sys.argv) != 2:
                   print("please enter the correct trace file to continue")
                   exit()
            else:
                
                 print("\nexecuting the trace",sys.argv[1])
                 fil=sys.argv[1]
        
                 private=two=three=four=five=six=seven=eight=nt=0
                
                 count=0
            
                 with open(fil) as f:
                       for line in f:
                             token=line.split(' ');
                             tid=int(token[0])
                             addres=int(token[1])
                             addr=(addres-(addres%64))
                             count+=1
                             profshare(tid,addr)
                             
                 
                 for key,value in memblk.items():
                       if len(value)==1:
                         private+=1
                       elif len(value)==2:
                         two+=1
                       elif len(value)==3:
                         three+=1
                       elif len(value)==4:
                         four+=1
                       elif len(value)==5:
                         five+=1
                       elif len(value)==6:
                         six+=1
                       elif len(value)==7:
                         seven+=1
                       elif len(value)==8:
                         eight+=1
                       else:
                         nt+=1
                 
                 total=private+two+three+four+five+six+seven+eight
                 outfile="sharing_profile.txt"
                 with open(outfile,"a") as g:
                      g.write('Executing Trace : %s\n'% fil )
                      g.write("total mem blocks is %s\n"% mb)
                      
                      g.write("private: %s\ttwo: %s\tthree: %s\tfour: %s\tfive: %s\tsix: %s\tseven: %s\teight: %s\n" % (private,two,three,four,five,six,seven,eight))
                      g.write("threads total:  %s\n" % str(total))
                      g.write("\n.......................................................\n\n")
            #("total",total)
             #    print("private",private,"\ttwo",two,"\tthree",three,"\tfour",four,"\tfive",five,"\tsix",six,"\tseven",seven,"\teight",eight)
        
if __name__ == "__main__":
    main()

