/*Sort encoded data w/o decoding & encoding it */
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <unistd.h>   //Defines standard symbolic constants and types
#include <sys/stat.h> //Defines the structures of fstat() and stat() 

int comparisonCounter = 0;
int rot13cmp(char const* a, char const* b)
{
  comparisonCounter++;
  int i = 0;

  while(1)
    {
      //Compare one char at a time

      //End of file comparisons
      if (a[i] == '\n')
	{
	  if (b[i] == '\n')
	    return 0;
	  return -1;
	}

      if (b[i] == '\n')
	return 1;

      //Check character by character once we have a difference
      if (a[i] != b[i])
	{
	  //For alphabetic cs that have the same case, logic is reversed since
	  // we switch sides and if sides are the same, normal evaluation
	  //results.
	  if (isalpha(a[i]) && isalpha(b[i]))
	    {
	      //Check to see if they have different cases first
	      if(isupper(a[i]) && islower(b[i]))
		return -1;
	      else if(islower(a[i]) && isupper(b[i]))
		return 1;

	      //Otherwise, they are the same case and logic will be reversed
	      else
		{
		  //Normal evaluation
		  if ((toupper(a[i]) >= 'A' && toupper(a[i]) <= 'M') && (toupper(b[i]) >= 'A' && toupper(b[i]) <= 'M'))
		    {
		      if (a[i] < b[i])
			return -1;
		      else
			return 1;
		    }

		  else if ((toupper(a[i]) >= 'N' && toupper(a[i]) <= 'Z') && (toupper(b[i]) >= 'N' && toupper(b[i]) <= 'Z'))
		    {
		      if (a[i] < b[i])
			return -1;
		      else
			return 1;
		    }

		  //Otherwise, we flip the logic since a and b are not in the same domain
		  if(a[i] < b[i])
		    return 1;
		  else
		    return -1;
		}
	    }

	  //Otherwise, evaluate normally because we have one or more non-alphabetic characters
	  if (a[i] < b[i])
	    return -1;
	  else
	    return 1;
	}

      i++;
    }
}

int cmp(const void *a, const void *b)
{
  return rot13cmp(*(const char**) a, *(const char**) b);
}

int main()
{
  struct stat filestats; //Creates a variable to get file status
  char c; //Input character
  char* input = &c; //Initializes a C-string to the input character address.
  int inputSize = 0;

  fstat(0, &filestats); //Obtains information about filestats for stdin.

  //If the file is regular, then set a static size. Else, set it as 2000 bytes 
  if (S_ISREG(filestats.st_mode))
    inputSize = filestats.st_size;
  else
    inputSize = 2000;

  input = (char*)malloc(inputSize);

  //Note: All the error messages will use a system call to write
  if (input == NULL) //Returns an error if input is NULL
    {
      char *errorMessage1 = "Error allocating buffer bytes";
      write (2, errorMessage1, sizeof(errorMessage1));
      exit(1);
    }

  int is_empty = 1;//Boolean used to check whether the file is empty
  int count = 0;//Counter used for indexing in my dynamically allocated array

  while(read(0, &input[count], 1) > 0)
    {
      is_empty = 0;//Let's us know we put something into the file
      count++;

      //Reallocate the size if necessary.
      if (count >= inputSize)
	{
	  inputSize += 2000; //Adjust size for future reallocations
	  input = (char*)realloc(input, inputSize);

	  if (input == NULL) //Returns an error if input is NULL
	    {
	      char *errorMessage2 = "Error when using realloc.";
	      write(2, errorMessage2, sizeof(errorMessage2));
	      exit(1);
	    }
	}
    }

  //Check if empty file was passed in
  if (is_empty)
    exit(0);

  //Append a newline at the end if there is no trailing newline
  if (input[count-1] != '\n')
      input[count] = '\n';

//Array of character pointers that point to words in input, space corresponds 
//to number of newlines
  char **helper_array;
  int helper_array_size = sizeof(char*) * 2000; 
  helper_array = (char**) malloc(helper_array_size);

  if (helper_array == NULL)//Returns an error if input is NULL
    {
      char *errorMessage3 = "Error when using 'helper_array' malloc.";
      write(2, errorMessage3, sizeof(errorMessage3));
      exit(1);
    }

  //Assign character pointers into each word of the array based on newlines
  
  helper_array[0] = &input[0]; //Map the start of the helper array to the first
  // address of input
  int i = 1, helper_array_i = 1;

  //Move all the characters from the input array into the helper_array
  //i++ will increment normally, helper_array_i++ increments number of indices
  //in the array
  while (i < count)
    {
      if (input[i] == EOF)
	break;
      //Check for newline characters
      if (input[i-1] == '\n' && input[i] != '\n')
	{
	  //Resize if necessary, the if condition was explained on Piazza. It
	  //has to do with the logic of how a double pointer works
	  if (sizeof(helper_array)*helper_array_i >= helper_array_size)
	    {
	      helper_array_size += sizeof(char*)*2000;
	      helper_array = (char**)realloc(helper_array, helper_array_size);
	    
	      if (helper_array == NULL)
	      {
		char *errorMessage4 = "Error when reallocating 'helper_array'";
		write(2, errorMessage4, sizeof(errorMessage4));
		exit(1);
	      }
	    }

	  helper_array[helper_array_i] = &input[i]; //Readjust the index of the
	  // helper array and the original array address
	  helper_array_i++;
	}
     
      i++;
    }
  
  //qsort will be the sorting algorithm used in this program
  qsort(helper_array, helper_array_i, sizeof(char*), cmp);

  //Use write to print out the encoded but sorted array
  for (i = 0; i < helper_array_i; i++)
    {
      while (write(1, helper_array[i], 1) > 0)
	{
	  //Break out if you encounter a newline character. Else, keep 
	  //incrementing the double character pointer
	   if (*(helper_array[i]) =='\n')
	     break;
	   helper_array[i]++;
	}
    }

  fprintf(stderr, "Number of comparisons: %i\n", comparisonCounter);

  //Free any allocated memory
  free(input);
  free(helper_array);
  exit(0);
}

