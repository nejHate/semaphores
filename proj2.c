#include <fcntl.h>
#include <semaphore.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

int strtoint(char *str) {
  if (str == NULL) return -1;
  if (str[0] == '\0') return -1;
  int number = 0;
  for (int i = 0; str[i] != '\0'; i++) {
    if (str[i] < '0' || str[i] > '9') {
      return -1;
    }
    number = number * 10 + (str[i] - '0');
  }
  return number;
}

void customer(int id, int TZ, sem_t *print_semaphore, int *A, FILE *output, int *queue, sem_t *queue_semaphore, sem_t **array_queue_semaphore, int *FS) {
  srand(time(NULL) + id);

  sem_wait(print_semaphore);
  fprintf(output, "%d: Z %d: started\n", ++(*A), id);
  fflush(output);
  sem_post(print_semaphore);

  usleep(rand() % (TZ * 1000 + 1));

  sem_wait(queue_semaphore);

  if (*FS == 1) {
    int service = rand() % 3 + 1;
    ++(queue[service - 1]);

    sem_wait(print_semaphore);
    fprintf(output, "%d: Z %d: entering office for a service %d\n", ++(*A), id, service);
    fflush(output);
    sem_post(print_semaphore);

    sem_post(queue_semaphore);

    sem_wait(array_queue_semaphore[service - 1]);

    sem_wait(print_semaphore);
    fprintf(output, "%d: Z %d: called by office worker\n", ++(*A), id);
    fflush(output);
    sem_post(print_semaphore);

    usleep(rand() % (10001));

  } else {

    sem_post(queue_semaphore);
  }

  sem_wait(print_semaphore);
  fprintf(output, "%d: Z %d: going home\n", ++(*A), id);
  fflush(output);
  sem_post(print_semaphore);

  sem_close(print_semaphore);
  sem_close(queue_semaphore);
  sem_close(array_queue_semaphore[0]);
  sem_close(array_queue_semaphore[1]);
  sem_close(array_queue_semaphore[2]);
  munmap(A, sizeof(int));
  munmap(queue, sizeof(int) * 3);
  munmap(FS, sizeof(int));
  fclose(output);
  exit(0);
}

void staff(int id, int TU, sem_t *print_semaphore, int *A, FILE *output, int *queue, sem_t *queue_semaphore, sem_t **array_queue_semaphore, int *FS) {
  srand(time(NULL) + id);

  sem_wait(print_semaphore);
  fprintf(output, "%d: U %d: started\n", ++(*A), id);
  fflush(output);
  sem_post(print_semaphore);

  int service = 0;

  while (1) {

    sem_wait(queue_semaphore);

    if (*FS == 0) {
      if (queue[0] + queue[1] + queue[2] == 0) {

        sem_post(queue_semaphore);

        break;
      }
    }

    if (queue[0] != 0) service = 1;
    else if (queue[1] != 0) service = 2;
    else if (queue[2] != 0) service = 3;
    else service = 0;
    
    if (service != 0) {
      --(queue[service - 1]);

      sem_wait(print_semaphore);
      fprintf(output, "%d: U %d: serving a service of type %d\n", ++(*A), id, service);
      fflush(output);
      sem_post(print_semaphore);

      sem_post(queue_semaphore);

      sem_post(array_queue_semaphore[service - 1]);

      usleep(rand() % (10001));

      sem_wait(print_semaphore);
      fprintf(output, "%d: U %d: service finished\n", ++(*A), id);
      fflush(output);
      sem_post(print_semaphore);

    } else {

      sem_wait(print_semaphore);
      fprintf(output, "%d: U %d: taking break\n", ++(*A), id);
      fflush(output);
      sem_post(print_semaphore);

      sem_post(queue_semaphore);

      usleep(rand() % (TU * 1000 + 1));

      sem_wait(print_semaphore);
      fprintf(output, "%d: U %d: break finished\n", ++(*A), id);
      fflush(output);
      sem_post(print_semaphore);
    }
  }

  sem_wait(print_semaphore);
  fprintf(output, "%d: U %d: going home\n", ++(*A), id);
  fflush(output);
  sem_post(print_semaphore);

  sem_close(print_semaphore);
  sem_close(queue_semaphore);
  sem_close(array_queue_semaphore[0]);
  sem_close(array_queue_semaphore[1]);
  sem_close(array_queue_semaphore[2]);
  munmap(A, sizeof(int));
  munmap(queue, sizeof(int) * 3);
  munmap(FS, sizeof(int));
  fclose(output);
  exit(0);
}

int main(int argc, char *argv[]) {

  if (argc != 6) {
    fprintf(stderr, "error, number of arguments is wrong\n"); // error
  }

  int NZ = strtoint(argv[1]); // počet zákazníků
  int NU = strtoint(argv[2]); // počet úředníků
  int TZ = strtoint(argv[3]); // zákazník wait
  int TU = strtoint(argv[4]); // úředník wait
  int F = strtoint(argv[5]);  // otvírací doba pošty
  
  if (NZ < 0 || NU < 1 || TZ < 0 || TU < 0 || F < 0) {
    fprintf(stderr, "error, one or more of the parametr was not writen good\n"); // error
    exit(1);
  }

  if (TZ > 10000 || TU > 100 || F > 10000) {
    fprintf(stderr, "error, TZ, TU or F fos bigger than can be\n"); // error
    exit(1);
  }

  FILE *output = fopen("proj2.out", "w");

  sem_unlink("xstepa74_print_semaphore");
  sem_unlink("xstepa74_queue_semaphore");
  sem_unlink("xstepa74_queue1_semaphore");
  sem_unlink("xstepa74_queue2_semaphore");
  sem_unlink("xstepa74_queue3_semaphore");

  sem_t *print_semaphore;
  print_semaphore = sem_open("xstepa74_print_semaphore", O_CREAT, 0644, 1);

  sem_t *queue_semaphore;
  queue_semaphore = sem_open("xstepa74_queue_semaphore", O_CREAT, 0644, 1);

  sem_t *queue1_semaphore;
  sem_t *queue2_semaphore;
  sem_t *queue3_semaphore;
  queue1_semaphore = sem_open("xstepa74_queue1_semaphore", O_CREAT, 0644, 0);
  queue2_semaphore = sem_open("xstepa74_queue2_semaphore", O_CREAT, 0644, 0);
  queue3_semaphore = sem_open("xstepa74_queue3_semaphore", O_CREAT, 0644, 0);

  if(queue1_semaphore == SEM_FAILED || queue2_semaphore == SEM_FAILED || queue3_semaphore == SEM_FAILED || print_semaphore == SEM_FAILED || queue_semaphore == SEM_FAILED){
    sem_close(print_semaphore);
    sem_close(queue_semaphore);
    sem_close(queue1_semaphore);
    sem_close(queue2_semaphore);
    sem_close(queue3_semaphore);
    fprintf(stderr, "error, while creating semaphores\n");
    fclose(output);
  }

  sem_t *array_queue_semaphores[] = {queue1_semaphore, queue2_semaphore, queue3_semaphore};

  int *A = mmap(NULL, sizeof(int), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
  if (A == MAP_FAILED) {
    sem_close(print_semaphore);
    sem_close(queue_semaphore);
    sem_close(queue1_semaphore);
    sem_close(queue2_semaphore);
    sem_close(queue3_semaphore);
    fprintf(stderr, "error\n"); // error
    exit(1);
  }

  int *queue = mmap(NULL, sizeof(int) * 3, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
  if (queue == MAP_FAILED) {
    sem_close(print_semaphore);
    sem_close(queue_semaphore);
    sem_close(queue1_semaphore);
    sem_close(queue2_semaphore);
    sem_close(queue3_semaphore);
    fprintf(stderr, "error, creating a shared memory for queue failed\n"); // error
    munmap(A, sizeof(int));
    exit(1);
  }

  int *FS = mmap(NULL, sizeof(int), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
  if (FS == MAP_FAILED) {
    sem_close(print_semaphore);
    sem_close(queue_semaphore);
    sem_close(queue1_semaphore);
    sem_close(queue2_semaphore);
    sem_close(queue3_semaphore);
    fprintf(stderr, "error, creating a shared memory for queue failed\n"); // error
    munmap(A, sizeof(int));
    munmap(queue, sizeof(int) * 3);
    exit(1);
  }
  *FS = 1;

  //creating processes
  for (int i = 0; i < NZ; i++) {
    if (fork() == 0) {
      customer(i + 1, TZ, print_semaphore, A, output, queue, queue_semaphore, array_queue_semaphores, FS);
    }
  }

  for (int i = 0; i < NU; i++) {
    if (fork() == 0) {
      staff(i + 1, TU, print_semaphore, A, output, queue, queue_semaphore, array_queue_semaphores, FS);
    }
  }

  srand(time(NULL) + NU + NZ); // initialize random number seed
  usleep(rand() % (F * 1000 + 1) + F*1000);

  sem_wait(queue_semaphore);

  sem_wait(print_semaphore);
  //close the 
  *FS = 0;
  fprintf(output, "%d: closing\n", ++(*A));
  fflush(output);

  sem_post(print_semaphore);

  sem_post(queue_semaphore);

  while (wait(NULL) != -1)
    ; // wait until all kids die
  //clear all memory and semaphores
  fclose(output);
  munmap(A, sizeof(int));
  munmap(queue, sizeof(int) * 3);
  munmap(FS, sizeof(int));
  sem_close(print_semaphore);
  sem_close(queue_semaphore);
  sem_close(queue1_semaphore);
  sem_close(queue2_semaphore);
  sem_close(queue3_semaphore);
}
