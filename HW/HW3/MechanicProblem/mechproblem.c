#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

// Semaphores for each tool
sem_t toolA, toolB, toolC;

void* mechanic1(void* arg) {
    while(1) {
        // Mechanic 1 needs tools A, B, and C
        sem_wait(&toolA);
        sem_wait(&toolB);
        sem_wait(&toolC);

        printf("Mechanic 1 is repairing using tools A, B, and C\n");
        sleep(1);  // Simulate time taken to repair the part

        sem_post(&toolC);
        sem_post(&toolB);
        sem_post(&toolA);
        
        printf("Mechanic 1 is taking a break\n");
        sleep(1);  // Simulate break time
    }
}

void* mechanic2(void* arg) {
    while(1) {
        // Mechanic 2 needs tools A and C
        sem_wait(&toolA);
        sem_wait(&toolC);

        printf("Mechanic 2 is repairing using tools A and C\n");
        sleep(1);  // Simulate time taken to repair the part

        sem_post(&toolC);
        sem_post(&toolA);
        
        printf("Mechanic 2 is taking a break\n");
        sleep(1);  // Simulate break time
    }
}

void* mechanic3(void* arg) {
    while(1) {
        // Mechanic 3 needs tools B and C
        sem_wait(&toolB);
        sem_wait(&toolC);

        printf("Mechanic 3 is repairing using tools B and C\n");
        sleep(1);  // Simulate time taken to repair the part

        sem_post(&toolC);
        sem_post(&toolB);
        
        printf("Mechanic 3 is taking a break\n");
        sleep(1);  // Simulate break time
    }
}

int main() {
    pthread_t t1, t2, t3;

    // Initialize semaphores
    sem_init(&toolA, 0, 1);
    sem_init(&toolB, 0, 1);
    sem_init(&toolC, 0, 1);

    // Create threads for each mechanic
    pthread_create(&t1, NULL, mechanic1, NULL);
    pthread_create(&t2, NULL, mechanic2, NULL);
    pthread_create(&t3, NULL, mechanic3, NULL);

    // Join threads (though in this example, the threads run infinitely)
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    pthread_join(t3, NULL);

    // Destroy semaphores
    sem_destroy(&toolA);
    sem_destroy(&toolB);
    sem_destroy(&toolC);

    return 0;
}
