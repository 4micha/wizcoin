"""Forest Fire Sim, by Al Sweigart
A simulation of wildfires spreading in a forest.
Press Ctrl-C to stop.
Tags: short, bext, simulation"""


import random, sys, time

try:
    import bext
except ImportError:
    print('This program requires the bext module, which you')
    print('can install by following the instructions at')
    print('https://pypi.org/project/Bext/')
    sys.exit()

# set up the constants
WIDTH = 200
HEIGHT = 80

TREE = 'A'
FIRE = 'W'
EMPTY = ' '

# try changing these settings to anything between 0.0 and 1.0
INITIAL_TREE_DENSITY = 0.20  # amount of forest that starts with trees
GROW_CHANCE = 0.01  # chance a blank space turns into a tree.
FIRE_CHANCE = 0.01  # chance a tree is hit by lightning & burns

# try setting the pause length from 0.5 to 1.0 or 0.0
PAUSE_LENGTH = 0.5


def main():
    forest = createNewForest()
    bext.clear()

    while True:  # main program loop
        displayForest(forest)

        # run a single simulation step
        nextForest = {'width': forest['width'],
                      'height': forest['height']}

        for x in range(forest['width']):
            for y in range(forest['height']):
                if (x, y) in nextForest:
                    # if we've already set nextForest[(x, y)] on a
                    # previous iteration, just do nothing here
                    continue

                if ((forest[(x, y)] == EMPTY) and (random.random() <= GROW_CHANCE)):

                    # grow a tree in this empty space
                    nextForest[(x, y)] = TREE
                elif ((forest[(x, y)] == TREE) and (random.random() <= FIRE_CHANCE)):

                    # lightning sets this tree on fire
                    nextForest[(x, y)] = FIRE
                elif forest[(x, y)] == FIRE:
                    # this tree is currently burning
                    # loop through all the neighboring spaces
                    for ix in range(-1, 2):
                        for iy in range(-1, 2):
                            # fire spreeds to neighboring trees
                            if forest.get((x + ix, y + iy)) == TREE:
                                nextForest[(x + ix, y + iy)] = FIRE
                                # the tree has burned down now, so erase it
                    nextForest[(x, y)] = EMPTY
                else:
                    # just copy the existing object
                    nextForest[(x, y)] = forest[(x, y)]
        forest = nextForest

        time.sleep(PAUSE_LENGTH)


def createNewForest():
    """returns a dictionary for a new forest data structure"""
    forest = {'width': WIDTH, 'height': HEIGHT}
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if (random.random() * 100) <= INITIAL_TREE_DENSITY:
                forest[(x, y)] = TREE  # start as a tree
            else:
                forest[(x, y)] = EMPTY  # start as an empty space
    return forest


def displayForest(forest):
    """display the forest data structure in the screen"""
    bext.goto(0, 0)
    for y in range(forest['height']):
        for x in range(forest['width']):
            if forest[(x, y)] == TREE:
                bext.fg('green')
                print(TREE, end='')
            elif forest[(x, y)] == FIRE:
                bext.fg('red')
                print(FIRE, end='')
            elif forest[(x, y)] == EMPTY:
                print(EMPTY, end='')
        print()
    bext.fg('reset')  # use the default font color
    print('Grow chance: {}%  '.format(GROW_CHANCE * 100), end='')
    print('Lightning chance: {}%  '.format(FIRE_CHANCE * 100), end='')
    print('Press Ctrl-C to quit.')


# if the program was run (instead of imported), run the game
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()  # when Ctrl-C is pressed, end the program