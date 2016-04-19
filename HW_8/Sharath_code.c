#include <pthread.h>
#include <stdio.h>

void* ThreadFunction(void *arg)
{
  long tID = (long)arg;
  printf("Inside thread function with ID = %ld\n", tID);
  pthread_exit(0);
}

int main()
{
  pthread_t threadID[5];
  long t;
  for (t = 0; t < 5; ++t)
    {
      int rs = pthread_create(&threadID[t], 0, ThreadFunction, (void*) t);
      if (rs){
	fprintf(stderr, "Error creating thread\n");
	return -1;
      }
    }
  
  printf("Main thread finished creating threads\n");
  for (t = 0; t < 5; ++t){
    void *retVal;
    int rs = pthread_join(threadID[t], &retVal);
    if(rs) {
      fprintf(stderr, "Error joining thread\n");
      return -1;
    }
  }
}
