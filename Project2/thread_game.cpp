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

//***************************************************************************************************
// MUTEX AND CONDITIONS*******************************************************************************
//***************************************************************************************************
pthread_mutex_t mutex;
pthread_cond_t turn_cond;
pthread_cond_t dealer_delt_cond;
// pthread_cond_t round_won_cond = PTHREAD_ maybe not needed
//***************************************************************************************************
//***************************************************************************************************
//***************************************************************************************************

//***************************************************************************************************
// SHARED REOURCES***********************************************************************************
//***************************************************************************************************
int deck[NUM_CARDS];     // Global deck
int deckIndex = 0;       // Global current card index representing the current card selected from the deck
int targetCard = 0;      // Global target card for the round
bool roundWon = false;   // Global flag to indicate if the round has been won
bool dealerDelt = false; // Global flag to indicate if the dealer has delt the cards
int currentPlayer = 0;   // Global current player to take action
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

// function prototypes
void initDeck();
void shuffleDeck();
void *playerPlay(void *arg);
void handleDealerTurn(int currentPlayerNum);
void handlePlayerTurn(player_account *playerAccount, int roundNum);

//***************************************************************************************************
// MAIN***********************************************************************************************
//***************************************************************************************************
int main(int argc, char *argv[])
{
    pthread_attr_t attr; // Set of thread attributes
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
    // Initialize attr
    pthread_attr_init(&attr);
    pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);
    // Initialize mutex and condition variables
    pthread_mutex_init(&mutex, NULL);
    pthread_cond_init(&turn_cond, NULL);
    pthread_cond_init(&dealer_delt_cond, NULL);

    for (int i = 0; i < NUM_PLAYERS; i++)
    {
        // initialize player numbers to playerThread index value to correlate playerThreads[player number] to playerAccount.id
        playerAccounts[i].playerNum = i;
        // initialize player into the game by creating the player threads
        pthread_create(&playerThreads[i], &attr, playerPlay, &playerAccounts[i]);
    }
    
    pthread_attr_destroy(&attr);
    
    for (int i = 0; i < NUM_PLAYERS; i++)
    {
        pthread_join(playerThreads[i], NULL);
    }
    // close file and destroy mutex and condition variables
    fclose(logFile);
    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&turn_cond);
    pthread_cond_destroy(&dealer_delt_cond);

    return 0;
}
//***************************************************************************************************
//***************************************************************************************************
//***************************************************************************************************

void *playerPlay(void *arg)
{ // player_account[playerNum].playerNum == playerAccount->playerNum
    // extract playerAccount from playerAccounts (array)
    player_account *playerAccount = (player_account *)arg;

    // extract playerNum from playerAccount
    int currentPlayerNum = playerAccount->playerNum;

    for (int roundNumber = 0; roundNumber < NUM_ROUNDS; roundNumber++)
    {
        // check to see if dealerDelt to start round for the dealer to deal cards or you are the dealer
        pthread_mutex_lock(&mutex);

        // wait until the dealer has delt the cards and it is your turn to play
        while (currentPlayer != currentPlayerNum)
        {
            pthread_cond_wait(&turn_cond, &mutex);
        }

        // check if youre the dealer
        if (currentPlayerNum == roundNumber % NUM_PLAYERS)
        {
            // handle the dealer turn
            handleDealerTurn(currentPlayerNum);
            // signal the next player to play

            // set the current player to the next player
            currentPlayer = (currentPlayerNum + 1) % NUM_PLAYERS;
            // signal the next player to play
            pthread_cond_broadcast(&turn_cond);
            pthread_mutex_unlock(&mutex);
            continue;
        }

        // check if the round has been won
        if (roundWon)
        {
            // you lost the round
            printf("PLAYER %d: Lost round %d\n", currentPlayerNum + 1, roundNumber + 1);
            fprintf(logFile, "PLAYER %d: Lost round %d\n", currentPlayerNum + 1, roundNumber + 1);
            // set the current player to the next dealer
            currentPlayer = (currentPlayerNum + 1) % NUM_PLAYERS;
            // signal the next player to play
            pthread_cond_broadcast(&turn_cond);
            pthread_mutex_unlock(&mutex);
            continue; // go to the next round
        }

        // it is your turn now if ur not the dealer
        if (currentPlayerNum != roundNumber % NUM_PLAYERS)
        {
            handlePlayerTurn(playerAccount, roundNumber);
        }
        // set the current player to the next player
        currentPlayer = (currentPlayerNum + 1) % NUM_PLAYERS;

        // Inside playerPlay function, at the end of the round loop
        if (roundNumber == NUM_ROUNDS - 1)
        {
            // Check if the currentPlayer is set correctly
            // Ensure that all players get to act in the final round
            // Consider adding logs here to debug the flow
            printf("Final round processing for player %d\n", currentPlayerNum+1);
        }

        // signal the next player to play
        pthread_cond_broadcast(&turn_cond);
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

void handlePlayerTurn(player_account *playerAccount, int roundNum)
{
    // get the current player number for ease
    int currentPlayerNum = playerAccount->playerNum;

    // check if round won
    if (roundWon)
    {
        // you lost the round
        printf("PLAYER %d: Lost asdfasdfround %d\n", currentPlayerNum + 1, roundNum + 1);
        fprintf(logFile, "PLAYER %d: Lost round %d\n", currentPlayerNum + 1, roundNum + 1);
    }
    else
    {
        // draw a card
        playerAccount->hand[1] = deck[deckIndex++];

        fprintf(logFile, "PLAYER %d: drew %d\n", currentPlayerNum + 1, playerAccount->hand[1]);
        fprintf(logFile, "PLAYER %d: <%d, %d>\n", currentPlayerNum + 1, playerAccount->hand[0], playerAccount->hand[1]);
        printf("PLAYER %d: drew %d\n", currentPlayerNum + 1, playerAccount->hand[1]);
        printf("PLAYER %d: <%d, %d>\n", currentPlayerNum + 1, playerAccount->hand[0], playerAccount->hand[1]);

        // check if you won the round
        if ((playerAccount->hand[0] == targetCard) || (playerAccount->hand[1] == targetCard))
        {
            // you won the round
            printf("PLAYER %d: wins round %d with matching card %d\n", currentPlayerNum + 1, roundNum + 1, targetCard);
            fprintf(logFile, "PLAYER %d: wins round %d with matching card %d\n", currentPlayerNum + 1, roundNum + 1, targetCard);
            // set round won to true
            roundWon = true;
        }
        else
        {
            // you did not win the round
            int discard = rand() % 2;
            printf("PLAYER %d: discards %d\n", currentPlayerNum + 1, playerAccount->hand[discard]);
            fprintf(logFile, "PLAYER %d: discards %d\n", currentPlayerNum + 1, playerAccount->hand[discard]);
        }
    }
}

void handleDealerTurn(int currentPlayerNum)
{
    // set round won to false we are about to start a new round
    roundWon = false;
    // shuffle the deck
    shuffleDeck();
    // draw target card
    targetCard = deck[deckIndex++];

    fprintf(logFile, "----------------------------------------------------\n");
    fprintf(logFile, "DEALER NUM: %d THE TARGET CARD: %d\n", currentPlayerNum + 1, targetCard);
    printf("----------------------------------------------------\n");
    printf("DEALER NUM: %d THE TARGET CARD: %d\n", currentPlayerNum + 1, targetCard);

    // deal 1 card to each player
    for (int i = 0; i < NUM_PLAYERS; i++) // may need to change this to only deal out to the players that are playing and not all players*************************************************8
    {
        playerAccounts[i].hand[0] = deck[deckIndex++]; // deal 1 card to player i and increment deck index
        fprintf(logFile, "DEALER NUM: %d DEALS %d TO PLAYER NUM: %d\n", currentPlayerNum + 1, playerAccounts[i].hand[0], i + 1);
        printf("DEALER NUM: %d DEALS %d TO PLAYER NUM: %d\n", currentPlayerNum + 1, playerAccounts[i].hand[0], i + 1);
    }
    // set dealer delt to true
    dealerDelt = true;
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