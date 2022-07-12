"""Langton's Ant, by Al Sweigart
A cellular automata animation. Press Ctrl-C to stop.
Tags: large, artistic, bext, simulation"""



import copy, random, sys, time

try:
    import bext
except ImportError:
    print('This program requires the bext module, which you')
    print('can install by following the instructions at')
    print('https://pypi.org/project/Bext/')
    sys.exit()

# set up the constants
WIDTH, HEIGHT = bext.size()
# we can't print to the last column on Windows without it adding a
# newline automatically, so reduce the width by one
WIDTH -= 1
HEIGHT -= 1  # adjustment for the quit message at the bottom

NUMBER_OF_ANTS = 30
PAUSE_AMOUNT = 0.05


ANT_UP = '^'
ANT_DOWN = 'v'
ANT_LEFT = '<'
ANT_RIGHT = '<'

# try to changing colors. bext module supports:
# black, red, green, yellow, blue, purple, cyan, white

ANT_COLOR = 'red'
BLACK_TILE = 'purple'
WHITE_TILE = 'black'

NORTH = 'north'
SOUTH = 'south'
EAST = 'east'
WEST = 'west'


def main():
    bext.fg(ANT_COLOR)  # the ants' color is the forground color
    bext.bg(WHITE_TILE)  # set the background to white to start
    bext.clear()

    # create a new board data structure
    board = {'width': WIDTH, 'height': HEIGHT}

    # create ant data structures
    ants = []
    for i in range(NUMBER_OF_ANTS):
        ant = {
            'x': random.randint(0, WIDTH - 1),
            'y': random.randint(0, HEIGHT - 1),
            'direction': random.choice([NORTH, SOUTH, EAST, WEST])
        }
        ants.append(ant)

    # keep track of which tiles have changed and need to be redrawn on
    # the screen
    changedTiles = []

    while True:  # main program loop
        displayBoard(board, ants, changedTiles)
        changedTiles = []

        # nextBoard is what the board will look like on the next step
        # in the simulation. Start with a copy of the current step's board
        nextBoard = copy.copy(board)

        # run a single simulation step for each ant
        for ant in ants:
            if board.get((ant['x'], ant['y']), False) == True:
                nextBoard[(ant['x'], ant['y'])] = False
                # turn clockwise
                if ant['direction'] == NORTH:
                    ant['direction'] = EAST
                elif ant['direction'] == EAST:
                    ant['direction'] = SOUTH
                elif ant['direction'] == SOUTH:
                    ant['direction'] = WEST
                elif ant['direction'] == WEST:
                    ant['direction'] = NORTH
            else:
                nextBoard[(ant['x'], ant['y'])] = True
                # turn counter clockwise
                if ant['direction'] == NORTH:
                    ant['direction'] = WEST
                elif ant['direction'] == EAST:
                    ant['direction'] = NORTH
                elif ant['direction'] == SOUTH:
                    ant['direction'] = EAST
                elif ant['direction'] == WEST:
                    ant['direction'] = SOUTH
            changedTiles.append((ant['x'], ant['y']))

            # move the ant forward in whatever direction it's facing
            if ant['direction'] == NORTH:
                ant['y'] -= 1
            elif ant['direction'] == EAST:
                ant['x'] += 1
            elif ant['direction'] == SOUTH:
                ant['y'] += 1
            elif ant['direction'] == WEST:
                ant['x'] -= 1

            # if the ant goes past the edge of the screen,
            # it should wrap around to other side
            ant['x'] = ant['x'] % WIDTH
            ant['y'] = ant['y'] % HEIGHT

            changedTiles.append((ant['x'], ant['y']))

        board = nextBoard


def displayBoard(board, ants, changedTiles):
    """Displays the board and ants on the screen. The changedTiles
    argument is a list of (x, y) tuples for tiles on the screen that
    have changed and need to be redrawn."""

    # draw the board data structure
    for x, y in changedTiles:
        bext.goto(x, y)
        if board.get((x, y), False):
            bext.bg(BLACK_TILE)
        else:
            bext.bg(WHITE_TILE)

        antIsHere = False
        for ant in ants:
            if (x, y) == (ant['x'], ant['y']):
                antIsHere = True
                if ant['direction']  == NORTH:
                    print(ANT_UP, end='')
                elif ant['direction'] == SOUTH:
                    print(ANT_DOWN, end='')
                elif ant['direction'] == EAST:
                    print(ANT_LEFT, end='')
                elif ant['direction'] == WEST:
                    print(ANT_RIGHT, end='')
                break
        if not antIsHere:
            print(' ', end='')

    # display the quit message at the bottom of the screen
    bext.goto(0, HEIGHT)
    bext.bg(WHITE_TILE)
    print('Press Ctrl-C to quit.', end='')

    sys.stdout.flush()  # (required for bext-using programs)
    time.sleep(PAUSE_AMOUNT)


# if this program was run (instead of imported), run the game
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Langton's Ant, by Al Sweigart")
        sys.exit()  # when Ctrl-C is pressed, end the program
