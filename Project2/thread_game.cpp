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

int deck[NUM_CARDS]; //Global deck
int deckIndex = 0; //Global current card index representing the current card selected from the deck
int targetCard = 0; //Global target card for the round
bool roundWon = false; //Global flag to indicate if the round has been won
int currentPlayer = 0; //Global current player to take action

//struct to represent a player that has an id and a hand of two cards
typedef struct {
    int id;
    int hand[2];
} player_account;
player_account playerManager[NUM_PLAYERS]; //Array of player accounts

int main(int argc, char *argv[])
{
    int seed = argc > 1 ? atoi(argv[1]) : time(NULL); //Seed for random number generator
    srand(seed);  // Seed the random number generator
    printf("Seed: %d\n", seed);

}