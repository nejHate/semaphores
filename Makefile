all: proj2

CFLAGS = -std=gnu99 -Wall -Wextra -Werror -pedantic -pthread -O3 -Wunused-variable

proj2: proj2.c
	gcc $(CFLAGS) proj2.c -o proj2
