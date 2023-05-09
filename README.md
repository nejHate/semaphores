# semaphores
synchronizing processes, shared memory, semaphores

the project takes 5 arguments
1) NZ: number of customers
2) NU: number of officers
3) TZ: time for customers
4) TU: time for officer
5) NZ time of post office to be open

after start:
main proces check the input parametres and turn them into int.
creates a semaphores and shared memory
using fork() it will
    -create NZ processes which will run customer function
    -create NU processes which will run officer function

main() then wait for NZ to 2*NZ miliseconds and close the post office and check untill all processes ends.

customer() will wait 0 to TZ milisecond and then, if the office is open, it enter the office for one of
the 3 services and wait. else it will go home. if it is in line and ofiicer choose the line, kernel choose
one of the waiting customers in the line and the customers will be served. after that it will go home.

staff() (officer) will look if somebody is in one of three services. if there is some customer,
it will choose non-empty line and start serving. it will write start serving and wait 0-10 miliseconds
and then return to start. if there is no customer it will take some break for
TU miliseconds and then return to start. if officer is at start and office is empty and office
is closed it will go home else it choose to serve a customer or take break.

the project proj2.c is compiled by Makefile and for checking is there python script
which will run compiled proj2.c. the script will ask to write 2 numbers. 1 is for how many
times should the script run and second ans for maximum threads for one type of functions (so
the maximum threads will be 2x + 1 (main)) and check the output and if there is error it will stop.
else it will continue. if there is deadlock it will stuck and the program must be killed.