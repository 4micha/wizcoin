"""Hourglass, by Al Sweigart
An animation of an hourglass with falling sand. Press Ctrl-C to stop.
Tags: large, artistic, bext, simulation"""


import random, sys, time

try:
    import bext
except ImportError:
    print('This program requires the bext modul, which you')
    print('can install by following the instructions at')
    print('https://pypi.org/project/Best/')
    sys.exit()

# set up the constants
PAUSE_LENGTH = 0.2
# (!) try to change this to any number between 0 and 100
WIDE_FALL_CHANCE = 50

SCREEN_WIDTH = 79
SCREEN_HEIGHT = 25
X = 0  # the index of X values in an (x, y) tuple is 0
Y = 1  # the index of Y values in an (x, y) tuple is 1
SAND = chr(9617)
WALL = chr(9608)

# set up the walls of the hourglass
HOURGLASS = set()  # has (x, y) tuples for where hourglass walls are

for i in range(18, 37):
    HOURGLASS.add((i, 1))  # add walls for the top cap of the hourglass
    HOURGLASS.add((i, 23))  # add walls for the bottom cap
for i in range(1, 5):
    HOURGLASS.add((18, i))  # top left straight wall
    HOURGLASS.add((36, i))
    HOURGLASS.add((18, i + 19))
    HOURGLASS.add((36, i + 19))
for i in range(8):
    HOURGLASS.add((19 + i, 5 + i))  # add the top left slanted wall
    HOURGLASS.add((35 - i, 5 + i))
    HOURGLASS.add((25 - i, 13 + i))
    HOURGLASS.add((29 + i, 13 + i))

# set up the initial sand at the top of the hourglass
INITIAL_SAND = set()
for y in range(8):
    for x in range(19 + y, 36 - y):
        INITIAL_SAND.add((x, y + 4))


def main():
    bext.fg('yellow')
    bext.clear()

    # draw the quit message
    bext.goto(0, 0)
    print('Ctrl-C to quit.', end='')

    # display the walls of the hourglass
    for wall in HOURGLASS:
        bext.goto(wall[X], wall[Y])
        print(WALL, end='')

    while True:  # main program loop
        allSand = list(INITIAL_SAND)

        # draw the initial sand
        for sand in allSand:
            bext.goto(sand[X], sand[Y])
            print(SAND, end='')

        runHourglassSimulation(allSand)


def runHourglassSimulation(allSand):
    """keep running the sand falling simulation until the sand stops
    moving"""
    while True:
        random.shuffle(allSand)  # random order of grain simulation

        sandMovedOnThisStep = False
        for i, sand in enumerate(allSand):
            if sand[Y] == SCREEN_HEIGHT - 1:
                # sand is on the very bottom, so it won't move
                continue

            # if nothing is under this sand, move it down
            noSandBelow = (sand[X], sand[Y] + 1) not in allSand
            noWallBelow = (sand[X], sand[Y] + 1) not in HOURGLASS
            canFallDown = noSandBelow and noWallBelow

            if canFallDown:
                # draw the sand in its new position down one space
                bext.goto(sand[X], sand[Y])
                print(' ', end='')
                bext.goto(sand[X], sand[Y] + 1)
                print(SAND, end='')

                # set the sand in its new position down one space
                allSand[i] = (sand[X], sand[Y] + 1)
                sandMovedOnThisStep = True
            else:
                # check if the sand can fall to the left
                belowLeft = (sand[X] - 1, sand[Y] + 1)
                noSandBelowLeft = belowLeft not in allSand
                noWallBelowLeft = belowLeft not in HOURGLASS
                left = (sand[X] - 1, sand[Y])
                noWallLeft = left not in HOURGLASS
                notOnLeftEdge = sand[X] > 0
                canFallLeft = (noSandBelowLeft and noWallBelowLeft
                               and noWallLeft and notOnLeftEdge)

                # check if the sand can fall to the right
                belowRight = (sand[X] + 1, sand[Y] + 1)
                noSandBelowRight = belowRight not in allSand
                noWallBelowRight = belowRight not in HOURGLASS
                right = (sand[X] + 1, sand[Y])
                noWallRight = right not in HOURGLASS
                notOnRightEdge = sand[X] < SCREEN_WIDTH - 1
                canFallRight = (noSandBelowRight and noWallBelowRight
                               and noWallRight and notOnRightEdge)

                # set the falling direction
                fallingDirection = None
                if canFallLeft and not canFallRight:
                    fallingDirection = -1  # set the sand to fall left
                elif not canFallLeft and canFallRight:
                    fallingDirection = 1
                elif canFallLeft and canFallRight:
                    # both possible, set randomly
                    fallingDirection = random.choice((-1, 1))

                # check if the sand can "far" fall two spaces to
                # the left or right instead of just one space
                if random.random() * 100 <= WIDE_FALL_CHANCE:
                    belowTwoLeft = (sand[X] - 2, sand[Y] + 1)
                    noSandBelowTwoLeft = belowTwoLeft not in allSand
                    noWallBelowTwoLeft = belowTwoLeft not in HOURGLASS
                    notOnSecondToLeftEdge = sand[X] > 1
                    canFallTwoLeft = (canFallLeft and noSandBelowTwoLeft
                                      and noWallBelowTwoLeft and notOnSecondToLeftEdge)

                    belowTwoRight = (sand[X] + 2, sand[Y] + 1)
                    noSandBelowTwoRight = belowTwoRight not in allSand
                    noWallBelowTwoRight = belowTwoRight not in HOURGLASS
                    notOnSecondToRightEdge = sand[X] < SCREEN_WIDTH - 2
                    canFallTwoRight = (canFallRight and noSandBelowTwoRight
                                      and noWallBelowTwoRight and notOnSecondToRightEdge)


                    if canFallTwoLeft and not canFallTwoRight:
                        fallingDirection = -2
                    elif not canFallTwoLeft and canFallTwoRight:
                        fallingDirection = 2
                    elif canFallTwoLeft and canFallTwoRight:
                        fallingDirection = random.choice((-2, 2))

                if fallingDirection == None:
                    # this sand can't fall, so move on
                    continue

                # draw the sand in its new position
                bext.goto(sand[X], sand[Y])
                print(' ', end='')
                bext.goto(sand[X] + fallingDirection, sand[Y] + 1)
                print(SAND, end='')

                # move the grain of sand to its new position
                allSand[i] = (sand[X] + fallingDirection, sand[Y] + 1)
                sandMovedOnThisStep = True

        sys.stdout.flush()  # required for bext-using programs
        time.sleep(PAUSE_LENGTH)

        # if no sand has moved on this step, reset the hourglass
        if not sandMovedOnThisStep:
            time.sleep(2)
            # erase all of the sand
            for sand in allSand:
                bext.goto(sand[X], sand[Y])
                print(' ', end='')
            break  # break out of main simulation loop


# if this program was run (instead of imported), run the game
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
