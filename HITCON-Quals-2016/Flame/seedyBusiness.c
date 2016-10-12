#include <stdio.h>
#include <stdlib.h>
#include <math.h>
int main()  /* Random number generator*/
{
 int i, n; /*initialize variables*/
 n = 40;   /*amount of numbers to be printed*/
 srand(7777);  /*initialized the random number generator*/
  for (i = 0; i < n; i++)
 {
   printf("%ld\n", random());
 }
 return(0);
}