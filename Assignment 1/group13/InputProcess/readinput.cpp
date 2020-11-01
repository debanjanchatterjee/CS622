#include <iostream>
#include<bits/stdc++.h>
#include <fstream>


using namespace std;


ofstream outfile;
int main(int argc, char const *argv[])
{
   int numtraces = atoi(argv[2]);
   const char * inputfilename = argv[1];
   const char * outputfilename = argv[3];
   FILE* fp;
   char* type, *iord;
   unsigned long long* addr;
   unsigned* pc;
   char input_name[1000];
   char out_name[1000];
   

   type = (char*)malloc(sizeof(char));
   iord = (char*)malloc(sizeof(char));
   addr = (unsigned long long*)malloc(sizeof(unsigned long long));
   pc   = (unsigned*)malloc(sizeof(unsigned));
   for (int k=0; k<numtraces; k++)
   {

     
      sprintf(input_name, "%s_%d", inputfilename, k);
      sprintf(out_name, "%s_%d", outputfilename, k);
      
      outfile.open(out_name);
      
      fp = fopen(input_name, "rb");
      assert(fp != NULL);

      while (!feof(fp)) {
         fread(iord, sizeof(char), 1, fp);
         fread(type, sizeof(char), 1, fp);
         fread(addr, sizeof(unsigned long long), 1, fp);
         fread(pc, sizeof(unsigned), 1, fp);


         outfile << (int)*type << " " << *addr << endl;


      }
      fclose(fp);
      outfile.close();

      printf("Done reading file %d!\n", k);
   }
   return 0;
}

