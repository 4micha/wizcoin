"""The Monty Hall Problem, by Al Sweigart
A simulation of the Monty Hall game show problem.


Tags: large, game, math, simulation"""

import random, sys

ALL_CLOSED = """
+------+  +------+  +------+
|      |  |      |  |      |
|   1  |  |   2  |  |   3  |
|      |  |      |  |      |
|      |  |      |  |      |
|      |  |      |  |      |
+------+  +------+  +------+"""

FIRST_GOAT = """
+------+  +------+  +------+
|  ((  |  |      |  |      |
|  oo  |  |   2  |  |   3  |
| /_/|_|  |      |  |      |
|    | |  |      |  |      |
|GOAT|||  |      |  |      |
+------+  +------+  +------+"""

SECOND_GOAT = """
+------+  +------+  +------+
|      |  |  ((  |  |      |
|   1  |  |  oo  |  |   3  |
|      |  | /_/|_|  |      |
|      |  |    | |  |      |
|      |  |GOAT|||  |      |
+------+  +------+  +------+"""

THIRD_GOAT = """
+------+  +------+  +------+
|      |  |      |  |  ((  |
|   1  |  |   2  |  |  oo  |
|      |  |      |  | /_/|_|
|      |  |      |  |    | |
|      |  |      |  |GOAT|||
+------+  +------+  +------+"""

FIRST_CAR_OTHERS_GOAT = """
+------+  +------+  +------+
| CAR! |  |  ((  |  |  ((  |
|    __|  |  oo  |  |  oo  |
|  _/  |  | /_/|_|  | /_/|_|
| /_ __|  |    | |  |    | |
|   O  |  |GOAT|||  |GOAT|||
+------+  +------+  +------+"""

SECOND_CAR_OTHERS_GOAT = """
+------+  +------+  +------+
|  ((  |  | CAR! |  |  ((  |
|  oo  |  |    __|  |  oo  |
| /_/|_|  |  _/  |  | /_/|_|
|    | |  | /_ __|  |    | |
|GOAT|||  |   O  |  |GOAT|||
+------+  +------+  +------+"""

THIRD_CAR_OTHERS_GOAT = """
+------+  +------+  +------+
|  ((  |  |  ((  |  | CAR! |
|  oo  |  |  oo  |  |    __|
| /_/|_|  | /_/|_|  |  _/  |
|    | |  |    | |  | /_ __|
|GOAT|||  |GOAT|||  |   O  |
+------+  +------+  +------+"""

print('''The Monty Hall Problem, by Al Sweigart

In the Monty Hall game show, you can pick one of three doors. One door
has a new car for a prize. The other two doors have worhless goats:
{}
Say you pick Door #1.
Before the door you choose is opend, another door with a goat is opened:
{}
You can choose to either open the door you originally picked or swap
to the other unopened door.

It may seem like it doesn't matter if swap or not, bur your odds
do improve if you swap doors! This program demonstrates the Monty Hall
problem by letting you do repeated experiments.

You can read an explanation of why swapping is better at
https://en.wikipedia.org/wiki/Monty_Hall_problem
'''.format(ALL_CLOSED, THIRD_GOAT))

input('Press Enter to start...')


swapWins = 0
swapLosses = 0
stayWins = 0
stayLosses = 0
while True:  # main program loop
    # the computer picks which door has the car
    doorThatHasCar = random.randint(1, 3)

    # ask the player to pick a door
    print(ALL_CLOSED)
    while True:  # keep asking the player until they enter a valid door
        print('Pick a door 1, 2, or 3 (or "quit" to stop):')
        response = input('> ').upper()
        if response == 'QUIT':
            # end the game
            print('Thanks for playing!')
            sys.exit()

        if response == '1' or response == '2' or response == '3':
            break
    doorPick = int(response)

    # figure out which goat door to show the player
    while True:
        # select a door that is a goat and not picked by the player
        showGoatDoor = random.randint(1, 3)
        if showGoatDoor != doorPick and showGoatDoor != doorThatHasCar:
            break

    # show this goat door to the player
    if showGoatDoor == 1:
        print(FIRST_GOAT)
    if showGoatDoor == 2:
        print(SECOND_GOAT)
    if showGoatDoor == 3:
        print(THIRD_GOAT)

    print('Door {} contains a goat!'.format(showGoatDoor))

    # ask the player if they want to swap
    while True:  # keep asking until the player enters Y or N.
        print('Do you want to swap doors? Y/N')
        swap = input('> ').upper()
        if swap == 'Y' or swap == 'N':
            break

    # swap the player's door if they wanted to swap
    if swap == 'Y':
        if doorPick == 1 and showGoatDoor == 2:
            doorPick = 3
        elif doorPick == 1 and showGoatDoor == 3:
            doorPick = 2
        elif doorPick == 2 and showGoatDoor == 1:
            doorPick = 3
        elif doorPick == 2 and showGoatDoor == 3:
            doorPick = 1
        elif doorPick == 3 and showGoatDoor == 1:
            doorPick = 2
        elif doorPick == 3 and showGoatDoor == 2:
            doorPick = 1

    # open all the doors
    if doorThatHasCar == 1:
        print(FIRST_CAR_OTHERS_GOAT)
    elif doorThatHasCar == 2:
        print(SECOND_CAR_OTHERS_GOAT)
    elif doorThatHasCar == 3:
        print(THIRD_CAR_OTHERS_GOAT)

    print('Door {} has the car!'.format(doorThatHasCar))

    # record wins and losses for swapping and not swapping
    if doorPick == doorThatHasCar:
        print('You won!')
        if swap == 'Y':
            swapWins += 1
        elif swap == 'N':
            stayWins += 1
    else:
        print('Sorry, you lost.')
        if swap == 'Y':
            swapLosses += 1
        elif swap == 'N':
            stayLosses += 1

    # calculate success rate of swapping and not swapping:
    totalSwaps = swapWins + swapLosses
    if totalSwaps != 0:  # prevent zero-divide error
        swapSuccess = round(swapWins / totalSwaps * 100, 1)
    else:
        swapSuccess = 0.0

    totalStays = stayWins + stayLosses
    if totalStays != 0:  # prevent zero-divide error
        staySuccess = round(stayWins / totalStays * 100, 1)
    else:
        staySuccess = 0.0

    print()
    print('Swapping:     ', end='')
    print('{} wins, {} losses, '.format(swapWins, swapLosses), end='')
    print('success rate {}%'.format(swapSuccess))
    print('Not swapping: ', end='')
    print('{} wins, {} losses, '.format(stayWins, stayLosses), end='')
    print('success rate {}%'.format(staySuccess))
    print()
    input('Press Enter to repeat the experiment...')
