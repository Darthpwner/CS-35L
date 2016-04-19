/*Sort encoded data w/o decoding & encoding it */
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

int rot13cmp(char const* a, char const* b)
{
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
  int size = 2000;//Arbitrary array size that I will adjust accordingly to the given input
  char *input = (char*) malloc(sizeof(char) * size);//Dynamically allocated array

  if (input == NULL) //Returns an error if input is NULL
    {
      fprintf(stderr, "Error when using 'input' malloc.");
      exit(1);
    }

  char c;//Input character
  int is_empty = 1;//Boolean used to check whether the file is empty
  int count = 0;//Counter used for indexing in my dynamically allocated array

  while(1)
    {
      c = getc(stdin);

      if (c == EOF)
	break;
      is_empty = 0;//Let's us know we put something into the file
      input[count] = c;
      count++;

      //Reallocate the size if necessary.
      if (count >= size)
	{
	  input = (char*)realloc(input, size*2);

	  if (input == NULL) //Returns an error if input is NULL
	    {
	      fprintf(stderr, "Error when using realloc.");
	      exit(1);
	    }

	  size *= 2;//Adjust size for future reallocations
	}
    }

  //Check if empty file was passed in
  if (is_empty)
    exit(0);

  //Append a newline at the end if there is no trailing newline
  if (input[count-1] != '\n')
    {
      input[count] = '\n';
      count++;
    }

  //Get the number of newlines for printing purposes
  int number_of_newlines = 0;
  int i;

  for (i = 0; i < count; i++)
    {
      if (input[i] == '\n')
	number_of_newlines++;
    }

  //Array of character pointers that point to words in input, space corresponds to number of newlines
  char **helper_array = (char**) malloc(sizeof(char*) * number_of_newlines);
  if (helper_array == NULL)//Returns an error if input is NULL
    {
      fprintf(stderr, "Error when using 'helper_array' malloc.");
      exit(1);
    }

  //Assign character pointers into each word of the array based on newlines
  int helper_array_i = 0;
  char *temp = input;

  //Move all the characters from the input array into the helper_array
  //i++ will increment normally, temp++ skips over any newline characters,
  //helper_array_i++ increments number of indices in the array
  for (i = 0; i < number_of_newlines; i++, temp++, helper_array_i++)
    {
      if (i == 0 && *temp == '\n')
	{
	  helper_array[helper_array_i++] = temp;//increments helper_array_i
	  //after this line executes
	  i++, temp++;
	}

      helper_array[helper_array_i] = temp;

      while (*temp != '\n')
	temp++;
    }

  //qsort will be the sorting algorithm used in this program
  qsort(helper_array, number_of_newlines, sizeof(char*), cmp);

  //Use putc to print out the encoded but sorted array
  char *c_temp;
  for (i = 0; i < number_of_newlines; i++)
    {
      c_temp = helper_array[i];
      int j = 0;

      while (1)
	{
	  if (c_temp[j] == '\n')
	    {
	      putc(c_temp[j], stdout);
	      j++;
	      break;
	    }

	  putc(c_temp[j], stdout);
	  j++;
	}
    }

  //Free any allocated memory
  free(input);
  free(helper_array);
  exit(0);
}

