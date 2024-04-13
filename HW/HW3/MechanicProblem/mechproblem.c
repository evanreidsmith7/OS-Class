#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>
#include <time.h>

// Semaphores for each tool
sem_t toolA, toolB, toolC;

// Shared variable to control loop termination
volatile int keepRunning = 1;

void *mechanic1(void *arg)
{
    time_t startTime = time(NULL);
    while (keepRunning)
    {
        printf("\nMechanic 1 waiting for tools\n");

        sem_wait(&toolA);
        sem_wait(&toolB);
        sem_wait(&toolC);

        printf("Mechanic 1 is repairing using tools A, B, and C\n");
        sleep(1); // Simulate time taken to repair the part
        printf("Mechanic 1 releasing tools\n");
    
        sem_post(&toolA);
        sem_post(&toolB);
        sem_post(&toolC);

        printf("Mechanic 1 is taking a break\n");
        sleep(1); // Simulate break time

        if (difftime(time(NULL), startTime) > 10)
        { // Run for 30 seconds
            keepRunning = 0;
        }
    }
    return NULL;
}

void *mechanic2(void *arg)
{
    time_t startTime = time(NULL);
    while (keepRunning)
    {
        printf("\nMechanic 2 waiting for tools\n");

        sem_wait(&toolA);
        sem_wait(&toolC);

        printf("Mechanic 2 is repairing using tools A and C\n");
        sleep(1);
        printf("Mechanic 2 releasing tools\n");

        sem_post(&toolA);
        sem_post(&toolC);

        printf("Mechanic 2 is taking a break\n");
        sleep(1);

        if (difftime(time(NULL), startTime) > 10)
        {
            keepRunning = 0;
        }
    }
    return NULL;
}

void *mechanic3(void *arg)
{
    time_t startTime = time(NULL);
    while (keepRunning)
    {
        printf("\nMechanic 3 waiting for tools\n");

        sem_wait(&toolB);
        sem_wait(&toolC);

        printf("Mechanic 3 is repairing using tools B and C\n");
        sleep(1);
        printf("Mechanic 3 releasing tools\n");

        sem_post(&toolB);
        sem_post(&toolC);

        printf("Mechanic 3 is taking a break\n");
        sleep(1);

        if (difftime(time(NULL), startTime) > 10)
        {
            keepRunning = 0;
        }
    }
    return NULL;
}

int main()
{
    pthread_t t1, t2, t3;

    // Initialize semaphores
    sem_init(&toolA, 0, 1);
    sem_init(&toolB, 0, 1);
    sem_init(&toolC, 0, 1);

    // Create threads for each mechanic
    pthread_create(&t1, NULL, mechanic1, NULL);
    pthread_create(&t2, NULL, mechanic2, NULL);
    pthread_create(&t3, NULL, mechanic3, NULL);

    // Wait for threads to finish
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    pthread_join(t3, NULL);

    // Destroy semaphores
    sem_destroy(&toolA);
    sem_destroy(&toolB);
    sem_destroy(&toolC);

    return 0;
}
