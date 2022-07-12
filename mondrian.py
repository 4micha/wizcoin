"""Mondrian Art Generator, by Al Sweigart
Randomly generates art in the style of Piet Mondrian


Tags: large, artistic, bext"""

import sys, random

try:
    import bext
except ImportError:
    print('This program requires the bext module, which you')
    print('can install by following the instructions at')
    print('https://pypi.org/project/Bext/')
    sys.exit()

# set up the constants
MIN_X_INCREASE = 6
MAX_X_INCREASE = 16
MIN_Y_INCREASE = 3
MAX_Y_INCREASE = 6
WHITE = 'white'
BLACK = 'black'
RED = 'red'
YELLOW = 'yellow'
BLUE = 'blue'

# setup the screen
width, height = bext.size()
# we cant't print to the last column on Windows without it adding a
# newline automatically, so reduce the width by one
width -= 1

height -= 3

while True:  # main applicatin loop
    # pre-populate the canvas with blank spaces
    canvas = {}
    for x in range(width):
        for y in range(height):
            canvas[(x, y)] = WHITE

    # generate vertical lines
    numberOfSegmentsToDelete = 0
    x = random.randint(MIN_X_INCREASE, MAX_X_INCREASE)
    while x < width - MIN_X_INCREASE:
        numberOfSegmentsToDelete += 1
        for y in range(height):
            canvas[(x, y)] = BLACK
        x += random.randint(MIN_X_INCREASE, MAX_X_INCREASE)

    # generate horizontal lines
    y = random.randint(MIN_Y_INCREASE, MAX_Y_INCREASE)
    while y < height - MIN_Y_INCREASE:
        numberOfSegmentsToDelete += 1
        for x in range(width):
            canvas[(x, y)] = BLACK
        y += random.randint(MIN_Y_INCREASE, MAX_Y_INCREASE)

    numberOfRectanglesToPaint = numberOfSegmentsToDelete - 3
    numberOfSegmentsToDelete = int(numberOfSegmentsToDelete * 1.5)

    # randomly select points and try to remove them
    for i in range(numberOfSegmentsToDelete):
        while True:  # keep selecting segments to try to delete
            # get a random start point on an existing segment
            startx = random.randint(1, width - 2)
            starty = random.randint(1, height - 2)
            if canvas[(startx, starty)] == WHITE:
                continue

            # find out if we're on a vertical or horizontal segment
            if (canvas[(startx - 1, starty)] == WHITE and
                canvas[(startx + 1, starty)] == WHITE):
                oriantation = 'vertical'
            elif (canvas[(startx, starty - 1)] == WHITE and
                canvas[(startx, starty + 1)] == WHITE):
                oriantation = 'horizontal'
            else:
                # the start point is on an intersection,
                # so we get a new random start point
                continue

            pointsToDelete = [(startx, starty)]

            canDeleteSegment = True
            if oriantation == 'vertical':
                # go up one path from the start point, and
                # see if we can remove this segment
                for changey in (-1, 1):
                    y = starty
                    while 0 < y < height - 1:
                        y += changey
                        if (canvas[(startx - 1, y)] == BLACK and
                            canvas[(startx + 1, y)] == BLACK):
                            # we've found a four-way intersection
                            break
                        elif ((canvas[(startx - 1, y)]  == WHITE and
                            canvas[(startx + 1, y)]  == BLACK) or
                            (canvas[(startx - 1, y)] == BLACK and
                            canvas[(startx + 1, y)] == WHITE)):
                            # we've found a T-intersection; we can't
                            # delete this segment
                            canDeleteSegment = False
                            break
                        else:
                            pointsToDelete.append((startx, y))

            elif oriantation == 'horizontal':
                # go up one path from the start point, and
                # see if we can remove this segment
                for changex in (-1, 1):
                    x = startx
                    while 0 < x < width - 1:
                        x += changex
                        if (canvas[(x, starty - 1)] == BLACK and
                                canvas[(x, starty + 1)] == BLACK):
                            # we've found a four-way intersection
                            break
                        elif ((canvas[(x, starty - 1)] == WHITE and
                               canvas[(x, starty + 1)] == BLACK) or
                              (canvas[(x, starty - 1)] == BLACK and
                               canvas[(x, starty + 1)] == WHITE)):
                            # we've found a T-intersection; we can't
                            # delete this segment
                            canDeleteSegment = False
                            break
                        else:
                            pointsToDelete.append((x, starty))
            if not canDeleteSegment:
                continue  # get a new random start point
            break  # move on to delete the segment

        # if we can delete this segment, set all the points to white
        for x, y in pointsToDelete:
            canvas[(x, y)] = WHITE

    # add the boarder lines
    for x in range(width):
        canvas[(x, 0)] = BLACK  # top boarder
        canvas[(x, height - 1)] = BLACK  # bottom boarder
    for y in range(height):
        canvas[(0, y)] = BLACK  # left boarder
        canvas[(width - 1, y)] = BLACK  # right boarder

    # paint the rectangles
    for i in range(numberOfRectanglesToPaint):
        while True:
            startx = random.randint(1, width - 2)
            starty = random.randint(1, height - 2)

            if canvas[(startx, starty)] != WHITE:
                continue  # get a new random start point
            else:
                break

        # flood fill algorithm
        colorToPaint = random.choice([RED, YELLOW, BLUE, BLACK])
        pointsToPaint = set([(startx, starty)])
        while len(pointsToPaint) > 0:
            x, y = pointsToPaint.pop()
            canvas[(x, y)] = colorToPaint
            if canvas[(x - 1, y)] == WHITE:
                pointsToPaint.add((x - 1, y))
            if canvas[(x + 1, y)] == WHITE:
                pointsToPaint.add((x + 1, y))
            if canvas[(x, y - 1)] == WHITE:
                pointsToPaint.add((x, y - 1))
            if canvas[(x, y + 1)] == WHITE:
                pointsToPaint.add((x, y + 1))

    # draw the canvas data structure
    for y in range(height):
        for x in range(width):
            bext.bg(canvas[(x, y)])
            print(' ', end='')

        print()

    # prompt user to create a new one
    try:
        input('Press Enter for another work of art, or Ctrl-C to quit.')
    except KeyboardInterrupt:
        sys.exit()