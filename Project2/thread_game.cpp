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
//***************************************************************************************************
//***************************************************************************************************
//***************************************************************************************************

//***************************************************************************************************
// SHARED REOURCES***********************************************************************************
//***************************************************************************************************
int deck[NUM_CARDS];     // Global deck
int deckIndex = 0;       // Global current card index representing the current card selected from the deck
int targetCard = 0;      // Global target card for the round
bool roundOver = false;  // Global flag to indicate if the round has been won
bool dealerDelt = false; // Global flag to indicate if the dealer has delt the cards
int roundNum = 0;        // Global current round number
//***************************************************************************************************
//***************************************************************************************************
//***************************************************************************************************

// struct to represent a player that has an id and a hand of two cards
typedef struct
{
    int playerNum;
    int hand[2]; // hands consist of two cards
    bool iWon = false;
} player_account;

player_account playerAccounts[NUM_PLAYERS]; // Array of player accounts

FILE *logFile; // output file

// function prototypes
void initDeck();
void shuffleDeck();
void *playerPlay(void *arg);
void *dealerDeal(void *arg);
void handleDealerTurn(int currentPlayerNum);
void handlePlayerTurn(player_account *playerAccount, int roundNum);
void printDeck(int deck[], int size);
void shiftDeckLeftAndAddDiscard(int discardedCard);

//***************************************************************************************************
// MAIN***********************************************************************************************
//***************************************************************************************************
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
    // Initialize mutex and condition variables
    pthread_mutex_init(&mutex, NULL);
    pthread_cond_init(&turn_cond, NULL);

    for (int i = 0; i < NUM_PLAYERS; i++)
    {
        // initialize player numbers to playerThread index value to correlate playerThreads[player number] to playerAccount.id
        playerAccounts[i].playerNum = i;
    }

    for (int round = 0; round < NUM_ROUNDS; round++)
    {
        // set the round number
        roundNum = round;
        // always start with the dealer
        pthread_create(&playerThreads[round], NULL, dealerDeal, (void *)&playerAccounts[round]);
        // wait for the dealer to finish
        pthread_join(playerThreads[round], NULL);

        // let the rest of the players take their turn one at a time
        for (int player = 0; player < NUM_PLAYERS; player++)
        {
            // start the thread for the player if it is not the dealer and the round is not over
            if (player != round && !roundOver)
            {
                pthread_create(&playerThreads[player], NULL, playerPlay, (void *)&playerAccounts[player]);
            }
            else
            {
                // skip the dealer
                continue;
            }
            // wait for the player to finish
            pthread_join(playerThreads[player], NULL);
        }

        // print the losers of the round
        for (int i = 0; i < NUM_PLAYERS; i++)
        {
            if ((playerAccounts[i].iWon == false) && (i != round))
            {
                //printf("PLAYER %d: lost round %d\n", i + 1, round + 1);
                fprintf(logFile, "PLAYER %d: lost round %d\n", i + 1, round + 1);
            }

            // reset the iWon flag for the next round
            playerAccounts[i].iWon = false;
        }
        //printf("DEALER NUM %d: Round Ends \n", round + 1);
    }
    fclose(logFile);
    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&turn_cond);

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

    // lock the mutex
    pthread_mutex_lock(&mutex);

    // draw a card
    playerAccount->hand[1] = deck[deckIndex++];

    fprintf(logFile, "PLAYER %d: drew %d\n", currentPlayerNum + 1, playerAccount->hand[1]);
    fprintf(logFile, "PLAYER %d HAND: <%d, %d>\n", currentPlayerNum + 1, playerAccount->hand[0], playerAccount->hand[1]);
    //printf("PLAYER %d: drew %d\n", currentPlayerNum + 1, playerAccount->hand[1]);
    printf("PLAYER %d HAND: <%d, %d>\n", currentPlayerNum + 1, playerAccount->hand[0], playerAccount->hand[1]);

    // check if you won the round
    if ((playerAccount->hand[0] == targetCard) || (playerAccount->hand[1] == targetCard))
    {
        // you won the round
        playerAccount->iWon = true;

        printf("PLAYER %d: wins round %d with matching card %d\n", currentPlayerNum + 1, roundNum + 1, targetCard);
        fprintf(logFile, "PLAYER %d: wins round %d with matching card %d\n", currentPlayerNum + 1, roundNum + 1, targetCard);
        // set round won to true
        roundOver = true;
    }
    else
    {
        // you did not win the round
        printf("PLAYER %d: loses round %d\n", currentPlayerNum + 1, roundNum + 1);

        int discard = rand() % 2;
        //printf("PLAYER %d: discards %d\n", currentPlayerNum + 1, playerAccount->hand[discard]);
        fprintf(logFile, "PLAYER %d: discards %d\n", currentPlayerNum + 1, playerAccount->hand[discard]);

        // shift the deck left and add the discarded card to the end
        shiftDeckLeftAndAddDiscard(playerAccount->hand[discard]);

        if (discard == 0)
        {

            fprintf(logFile, "PLAYER %d HAND: <%d>\n", currentPlayerNum + 1, playerAccount->hand[1]);
        }
        else
        {
            fprintf(logFile, "PLAYER %d HAND: <%d>\n", currentPlayerNum + 1, playerAccount->hand[0]);
        }

        // print the current deck
        printDeck(deck, NUM_CARDS);
    }

    // unlock the mutex
    pthread_mutex_unlock(&mutex);

    return NULL;
}
void *dealerDeal(void *arg)
{
    // extract playerAccount from playerAccounts (array)
    player_account *playerAccount = (player_account *)arg;

    // extract playerNum from playerAccount
    int currentPlayerNum = playerAccount->playerNum;

    // lock the mutex
    pthread_mutex_lock(&mutex);
    // set round won to false we are about to start a new round
    roundOver = false;
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

    // unlock the mutex
    pthread_mutex_unlock(&mutex);

    return NULL;
}
// Function to shift deck contents left and add discarded card to the end
void shiftDeckLeftAndAddDiscard(int discardedCard)
{
    // Shift all cards left by one position
    for (int i = 1; i < NUM_CARDS; ++i)
    {
        deck[i - 1] = deck[i];
    }
    // Add the discarded card to the end of the deck
    deck[NUM_CARDS - 1] = discardedCard;

    // adjust the deck index
    deckIndex--;
}

// Function to print the deck
void printDeck(int deck[], int size)
{
    printf("Deck: ");
    for (int i = deckIndex; i < size; ++i)
    {
        printf("%d ", deck[i]);
        fprintf(logFile, "%d ", deck[i]);
    }
    fprintf(logFile, "\n");
    printf("\n");
}

void handlePlayerTurn(player_account *playerAccount, int roundNum)
{
    // get the current player number for ease
    int currentPlayerNum = playerAccount->playerNum;
}

void handleDealerTurn(int currentPlayerNum)
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