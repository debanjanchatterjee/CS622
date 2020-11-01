#include <stdio.h>
#include "pin.H"
#include <assert.h>
#include <string.h>
FILE * trace, * tr_count;
PIN_LOCK pinLock;

UINT64 tracecount=0;
//print the memory access trace
VOID PrintTrace(THREADID tid,UINT64 addr, UINT32 size){

UINT64 memaccesssize=size;
UINT64 modval=addr%64;
UINT64 presentmemblockstart,presentmemblockend;


if(modval==0){
presentmemblockstart=addr;
presentmemblockend=addr+64;
}

if(modval!=0){
presentmemblockstart=addr-modval;
presentmemblockend=addr+(64-modval);
}

//2) if mem access size crosses the memory block boundary
//1) if mem access size is within the memory block 


//here is the code if addr+size falls inside the presentmemoryblock

if(addr+memaccesssize<=presentmemblockend || (addr==presentmemblockstart && memaccesssize<=64)){
	UINT blocksize=0;
	while(1){
	fprintf(trace,"%d %lu\n",tid,addr+blocksize);
	tracecount++;
	fflush(trace);
	blocksize+=8;
	if(blocksize>memaccesssize)
	{
		blocksize-=4;	
		if(blocksize>memaccesssize){
			blocksize-=2;
			if(blocksize>memaccesssize){
				blocksize-=1;
				if(blocksize>memaccesssize){
					fprintf(stdout, "ERROR: blocksize greater than memory access size\n");
					fflush(stdout);
					std::exit(0);
				}
			}	
		}	

	}
	if(blocksize==memaccesssize)break;
	}//close while loop

}
// done for 1) case
//code for 2) case i.e if the memory access size crosses the boundary
//two subcases 1)if memaccess crosses only 1 memory block boundary 
//2)if memaccess crosses multiple memory block boundaries


else{
UINT64 lastmemoryblockend=(addr+memaccesssize)-((addr+memaccesssize)%64);

UINT64 firstblockremaining=presentmemblockend-addr;
UINT64 lastblockremaining=memaccesssize;//for accurate blocksize values in the last block

//for first block remaining
UINT64 blocksize=0;
while(1)
	{
	fprintf(trace,"%d %lu\n",tid,addr+blocksize);
	tracecount++;
	fflush(trace);
	blocksize+=8;
	if(blocksize>firstblockremaining)
	{
		blocksize-=4;	
		if(blocksize>firstblockremaining){
			blocksize-=2;
			if(blocksize>firstblockremaining){
				blocksize-=1;
				if(blocksize>firstblockremaining){
					fprintf(stdout, "ERROR: blocksize greater than memory access size\n");
					fflush(stdout);
					std::exit(0);
				}
			}	
		}	

	}
	if(blocksize==firstblockremaining)break;
	}//done for first block cross

//if there are lots of entire blocks in between

if(presentmemblockend < lastmemoryblockend){
while(1){
	fprintf(trace,"%d %lu\n",tid,addr+blocksize);
	tracecount++;
	fflush(trace);
	blocksize+=8;
	if(addr+blocksize==lastmemoryblockend) break;
}
}

//now for last block
while(1)
{
	fprintf(trace,"%d %lu\n",tid,addr+blocksize);
	tracecount++;
	fflush(trace);
	blocksize+=8;
	if(blocksize>lastblockremaining)
	{
		blocksize-=4;	
		if(blocksize>lastblockremaining){
			blocksize-=2;
			if(blocksize>lastblockremaining){
				blocksize-=1;
				if(blocksize>lastblockremaining){
					fprintf(stdout, "ERROR: blocksize greater than memory access size\n");
					fflush(stdout);
					std::exit(0);
				}
			}	
		}	

	}
	if(blocksize==lastblockremaining)break;
}//end of while of last block

}
//fprintf(stdout,"total traces are:%lu",tracecount);
//fflush(stdout);
}



// Print a memory read record
VOID RecordMemRead(THREADID tid,VOID * ip, VOID * address,UINT32 size)
{
	UINT64 addr = reinterpret_cast<UINT64>(address);
	PIN_GetLock(&pinLock, tid+1);
	PrintTrace(tid,addr,size);
	PIN_ReleaseLock(&pinLock);
}

// Print a memory write record
VOID RecordMemWrite(THREADID tid,VOID * ip, VOID * address,UINT32 size)
{
	UINT64 addr = reinterpret_cast<UINT64>(address);
	PIN_GetLock(&pinLock, tid+1);
	PrintTrace(tid,addr,size);
	PIN_ReleaseLock(&pinLock);
}

// Is called for every instruction and instruments reads and writes
VOID Instruction(INS ins, VOID *v)
{
    // Instruments memory accesses using a predicated call, i.e.
    // the instrumentation is called iff the instruction will actually be executed.
    //
    // On the IA-32 and Intel(R) 64 architectures conditional moves and REP 
    // prefixed instructions appear as predicated instructions in Pin.
    UINT32 memOperands = INS_MemoryOperandCount(ins);
    
    // Iterate over each memory operand of the instruction.
    for (UINT32 memOp = 0; memOp < memOperands; memOp++)
    { 	
	UINT32 memopsize=INS_MemoryOperandSize(ins,memOp);
        if (INS_MemoryOperandIsRead(ins, memOp))
        {
            INS_InsertPredicatedCall(
                ins, IPOINT_BEFORE, (AFUNPTR)RecordMemRead,
		IARG_THREAD_ID,                
		IARG_INST_PTR,
                IARG_MEMORYOP_EA, memOp,
		IARG_UINT32,memopsize,
                IARG_END);
        }
        // Note that in some architectures a single memory operand can be 
        // both read and written (for instance incl (%eax) on IA-32)
        // In that case we instrument it once for read and once for write.
        if (INS_MemoryOperandIsWritten(ins, memOp))
        {
            INS_InsertPredicatedCall(
                ins, IPOINT_BEFORE, (AFUNPTR)RecordMemWrite,
		IARG_THREAD_ID,                
		IARG_INST_PTR,
                IARG_MEMORYOP_EA, memOp,
                IARG_UINT32,memopsize,
		IARG_END);
        }
    }
}


// This routine is executed every time a thread is created.
VOID ThreadStart(THREADID tid, CONTEXT *ctxt, INT32 flags, VOID *v)
{
    PIN_GetLock(&pinLock, tid+1);
    fprintf(stdout, "thread begin %d\n",tid);
    fflush(stdout);
    PIN_ReleaseLock(&pinLock);
}

// This routine is executed every time a thread is destroyed.
VOID ThreadFini(THREADID tid, const CONTEXT *ctxt, INT32 code, VOID *v)
{
    PIN_GetLock(&pinLock, tid+1);
    fprintf(stdout, "thread end %d code %d\n",tid, code);
    fflush(stdout);
    PIN_ReleaseLock(&pinLock);
}

VOID Fini(INT32 code, VOID *v)
{
    //fprintf(trace, "#eof\n");
    fprintf(tr_count," :%lu\n",tracecount);
	fflush(tr_count);
    fclose(trace);
    fclose(tr_count);
}

/* ===================================================================== */
/* Print Help Message                                                    */
/* ===================================================================== */
   
INT32 Usage()
{
    PIN_ERROR( "This Pintool prints a trace of memory addresses\n" 
              + KNOB_BASE::StringKnobSummary() + "\n");
    return -1;
}

/* ===================================================================== */
/* Main                                                                  */
/* ===================================================================== */

int main(int argc, char *argv[])
{
char *filename=argv[6];
strcat(filename,".out");
filename=filename+2;
trace = fopen(filename, "w");
tr_count=fopen("trace_counts.out","a");
fprintf(tr_count,"the trace count of the file %s is",filename);
fflush(tr_count);
PIN_InitLock(&pinLock);
    if (PIN_Init(argc, argv)) return Usage();

    
 
   
    INS_AddInstrumentFunction(Instruction, 0);

    PIN_AddThreadStartFunction(ThreadStart, 0);
    PIN_AddThreadFiniFunction(ThreadFini, 0);

    // Register Fini to be called when the application exits
    PIN_AddFiniFunction(Fini, 0);
    
    // Never returns
    PIN_StartProgram();
    
    return 0;
}
