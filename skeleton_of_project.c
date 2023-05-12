void zakaznik(----){
    srand(time(NULL) + id)
    printf("started")
    usleep()

    sem_wait(sem_pamet)
    if(opened){
        ++(mem_fronta[rand()]) //1 - 3
        print(entering office id X)
        sem_post()

        sem_wait(fronta_x)

        print(called by)

        usleep(rand()%(1000 + 1))

    }
    else{
        sem_post(sem_pamet)
    }
    
    print(going home)
    //clean semaphores and memory
    fclose()
    exit(0)

}



void urednik(){
    srand(time(NULL) + id)
    print(started)

    while(1){
        sem_wait(sem_pamet)
        if (opened == 0 && mem_opened == 0){
            break
        }

        x = rand()


        if (mem_open != 0){
            x = rand()
            --((mem_fronta[x]))
            print(serving service x)
            sem_post(sem_pamet)
            sem_post(fronta_x)

            usleep()

            print(service finished)
        }
        else{
            print(taking break)
            sem_post(sem_pamet)
            usleep()

            print(break finished)
        }
    }
    sem_post(sem_pamet)
    fclose()

    //clean all
}

void main(){
    sem_unlink("nazev_semaforu")
    sem_unlink("nazev_semaforu")
    sem_unlink("nazev_semaforu")



    srand(time(NULL))
    sem_open(A = 1)
    sem_open(sem_pamet = 1)
    sem_open(fronta1 = 0)
    sem_open(fronta2 = 0)
    sem_open(fronta3 = 0)

    mmap(mem_A)
    mmap(3 * mem_fronta)
    mmap(mem_opened)

    fork()
    fork()

    usleep()
    sem_wait(sem_pamet)
    mem_opened = 0
    print(closing)
    sem_post(sem_pamet)

    while(wait(NULL) != -1)
    --
    // clean all
}
