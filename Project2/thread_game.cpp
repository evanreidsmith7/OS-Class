/************************************************************************************
This program is a card game simulation using threads. Each thread represents a player
in the game. The game is played for 6 rounds, and each player has a hand of two cards.
The goal of the game is to match a target card set for each round by the dealer,who is
also one of the players in the game. (taking dealer turns each round) The game is
played in a round-robin fashion,where each player takes turns to play. The player
who matches the target card wins the round.
************************************************************************************
by Evan Smith
************************************************************************************/

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
using namespace std;

#define NUM_CARDS 52
#define NUM_PLAYERS 6
#define NUM_ROUNDS 6

// function prototypes
void initDeck();
void shuffleDeck();
void* playerPlay(void* arg);

//***************************************************************************************************
//MUTEX AND CONDITIONS*******************************************************************************
//***************************************************************************************************
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t turn_cond = PTHREAD_COND_INITIALIZER;
pthread_cond_t dealer_delt_cond = PTHREAD_COND_INITIALIZER;
//***************************************************************************************************
//***************************************************************************************************
//***************************************************************************************************

//***************************************************************************************************
//SHARED REOURCES************************************************************************************
//***************************************************************************************************
int deck[NUM_CARDS];   // Global deck
int deckIndex = 0;     // Global current card index representing the current card selected from the deck
int targetCard = 0;    // Global target card for the round
bool roundWon = false; // Global flag to indicate if the round has been won
int currentPlayer = 0; // Global current player to take action
//***************************************************************************************************
//***************************************************************************************************
//***************************************************************************************************


// struct to represent a player that has an id and a hand of two cards
typedef struct
{
    int playerNum;
    int hand[2]; // hands consist of two cards
} player_account;

player_account playerAccounts[NUM_PLAYERS]; // Array of player accounts

FILE *logFile; // output file

int main(int argc, char *argv[])
{
    int seed = argc > 1 ? atoi(argv[1]) : time(NULL); // Seed for random number generator
    srand(seed);                                      // Seed the random number generator
    printf("Seed: %d\n", seed);
    
    pthread_t playerThreads[NUM_PLAYERS]; // Array of player threads

    // Open log file
    logFile = fopen("log.txt", "w");
    if (logFile == NULL)
    {
        perror("Error opening log file");
        exit(1);
    }

    // Initialize the deck
    initDeck();

    for (int i = 0; i < NUM_PLAYERS; i++)
    {
        //initialize player numbers to playerThread index value to correlate playerThreads[player number] to playerAccount.id
        playerAccounts[i].playerNum = i;
        //initialize player into the game by creating the player threads
        //TODO: create player threads
    }
}

void* player_thread(void* arg)
{
    
}

void initDeck()
{
    for (int i = 0; i < NUM_CARDS; i++)
    {
        deck[i] = i % 13 + 1; // Cards from 1 to 13, simulating four suits
    }
    shuffleDeck(); // Initial shuffle
}

void shuffleDeck()
{
    for (int i = 0; i < NUM_CARDS; i++)
    {
        int j = rand() % (i + 1); // randomly selects a card with a value between 0 and i
        int temp = deck[i];
        deck[i] = deck[j];
        deck[j] = temp;
    }
    deckIndex = 0; // Reset deck index after shuffle
}