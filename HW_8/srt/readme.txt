I had a lot of trouble trying to find out how to start the homework. At first,
the code looked incredibly intimidating and heavily mathematical, so I was not
sure how to start off on the homework. In particular, the four nested four 
loops had a lot of lines of code that I did not understand. Fortunately, 
Ruolin helped me out and explained that the int values for "px" and "py" 
represent indices on a large array that would be laid out like a grid. He 
reassured me that I did not have to worry about the doubles "x" and "y" as 
well as the "halfSamples".

I also had another problem doing the dynamic memory allocation: I initially
thought the right syntax to do this was: "pthread_t tids = (pthread_t) 
malloc (sizeof(pthread_t) * nthreads);". Howeer, this was incorrect and Ruolin
reminded me that malloc takes a pointer and not a regular variable, so I 
simply added the star operator to make every instance of pthread_t in this 
context into a pointer. The exact syntax to make this correction was this: 
"pthread_t *tids = (ptrehad_t*) malloc(sizeof(pthread_t) * nthreads;", where
a pthread_t variable is assumed to have a size of 4 bytes like an int variable.

As soon as I ran this, I was getting a correct timing distribution where the 
correlation between the number of threads and the "real" time was inversely
proportional, but the problem was that the timing numbers were way off (8 
seconds vs. 46 seconds when I ran the original main.c file). It turns out my
entire algorithm for my function was wrong, so I scrapped my existing code and
reworked the algorithm. Tai-Lin Chu helped me a lot in this case on how to set
up the function; the biggest issue I had was that I did not create a separate
3-dimensional float to hold the scaled colors of the image. Upon creating this
and making additional structs to hold indices and integer id's, the program
began to run approximately 46 seconds for the 1-thread test case. 

The final issue I had was very trivial but pretty important for my sanity; I
forgot to include a printf statement to display the results to <n>-test.ppm, 
where <n> was the number of threads ranging from the input set {1, 2, 4, 8}.
Upon completing this, every part of the code ran as it should.

Implementing SRT improved the performance speed by a factor of 2 for each
additional step of parallelization. There was an inverse relationship between
the time it takes to execute the code and the number of threads, which makes 
sense because as you start dividing the work into more threads, execution 
should speed up because it is analagous to having more people designing a 
building. The data is shown here and is replicated in my "make-log.txt":

time ./srt 1-test.ppm >1-test.ppm.tmp && mv 1-test.ppm.tmp 1-test.ppm

real    0m46.811s
user    0m46.805s
sys     0m0.000s
time ./srt 2-test.ppm >2-test.ppm.tmp && mv 2-test.ppm.tmp 2-test.ppm

real    0m23.349s
user    0m46.392s
sys     0m0.002s
time ./srt 4-test.ppm >4-test.ppm.tmp && mv 4-test.ppm.tmp 4-test.ppm

real    0m12.204s
user    0m48.511s
sys     0m0.004s
time ./srt 8-test.ppm >8-test.ppm.tmp && mv 8-test.ppm.tmp 8-test.ppm

real    0m9.552s
user    0m59.178s
sys     0m0.003s
for file in 1-test.ppm 2-test.ppm 4-test.ppm 8-test.ppm; do \
          diff -u 1-test.ppm $file || exit; \
        done

As we can see for each of the four test cases, as we double the number of 
threads, the amount of time it takes to run these commands is cut in half. This
suggests an inverse linear relationship between the time it takes to execute
the commands and the number of threads used. 
