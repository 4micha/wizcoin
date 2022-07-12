"""Flooder, by Al Sweigart
A colorful game where you try to fill the board with a single color. Has
a mode for colorblind players.
Tags: large, bext, game"""



import random, sys

try:
    import bext
except ImportError:
    print('This program requires the bext module, which you')
    print('can install by following the instructions at')
    print('https://pypi.org/project/Bext/')
    sys.exit()

# set up the constants
BOARD_WIDTH = 16
BOARD_HEIGHT = 14
MOVES_PER_GAME = 20

# constants for the different shapes used in colorblind mode
HEART = chr(9829)
DIAMOND = chr(9830)
SPADE = chr(9824)
CLUB = chr(9827)
BALL = chr(9679)
TRIANGLE = chr(9650)

BLOCK = chr(9608)
LEFTRIGHT = chr(9472)
UPDOWN = chr(9474)
DOWNRIGHT = chr(9484)
DOWNLEFT = chr(9488)
UPRIGHT = chr(9492)
UPLEFT = chr(9496)


# all the color/shape tiles used on the board
TILE_TYPES = (0, 1, 2, 3, 4, 5)
COLORS_MAP = {0: 'red', 1: 'green', 2: 'blue',
              3: 'yellow', 4: 'cyan', 5: 'purple'}
COLOR_MODE = 'color mode'
SHAPES_MAP = {0: HEART, 1: TRIANGLE, 2: DIAMOND,
              3: BALL, 4: CLUB, 5: SPADE}
SHAPE_MODE = 'shape mode'


def main():
    bext.bg('black')
    bext.fg('white')
    bext.clear()
    print('''Flooder, by Al Sweigart
    
    Set the upper left color/shape, which fills in all the
    adjacent squares of that color/shape. Try to make the
    entire board the same color/shape.''')

    print('Do you want to play in colorblind mode? Y/N')
    response = input('> ')
    if response.upper().startswith('Y'):
        displayMode = SHAPE_MODE
    else:
        displayMode = COLOR_MODE

    gameBoard = getNewBoard()
    movesLeft = MOVES_PER_GAME

    while True:  # main game loop
        displayBoard(gameBoard, displayMode)

        print('Moves left:', movesLeft)
        playerMove = askForPlayerMove(displayMode)
        changeTile(playerMove, gameBoard, 0, 0)
        movesLeft -= 1

        if hasWon(gameBoard):
            displayBoard(gameBoard, displayMode)
            print('You have won!')
            break
        elif movesLeft == 0:
            displayBoard(gameBoard, displayMode)
            print('You have run out of moves!')
            break


def getNewBoard():
    """Return a dictionary of a new Flood It board"""

    # keys are (x, y) tuples, values are the tile at that position.
    board = {}

    # create random colors for the board
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            board[(x, y)] = random.choice(TILE_TYPES)

    # make severaltiles the same as their neighbor. this creates groups
    # of the same color/shape
    for i in range(BOARD_WIDTH * BOARD_HEIGHT):
        x = random.randint(0, BOARD_WIDTH - 2)
        y = random.randint(0, BOARD_HEIGHT - 1)
        board[(x + 1, y)] = board[x, y]
    return board


def displayBoard(board, displayMode):
    """display the board on the screen"""
    bext.fg('white')
    # display the top edge of the board
    print(DOWNRIGHT + (LEFTRIGHT * BOARD_WIDTH) + DOWNLEFT)

    # display each row
    for y in range(BOARD_HEIGHT):
        bext.fg('white')
        if y == 0:  # the first row begins with '>'
            print('>', end='')
        else:  # later rows begin with a white vertical line
            print(UPDOWN, end='')

        # display each tile in this row
        for x in range(BOARD_WIDTH):
            bext.fg(COLORS_MAP[board[(x, y)]])
            if displayMode == COLOR_MODE:
                print(BLOCK, end='')
            elif displayMode == SHAPE_MODE:
                print(SHAPES_MAP[board[(x, y)]], end='')

        bext.fg('white')
        print(UPDOWN)  # rows end with a white vertical line
    # display the bottom edge of the board
    print(UPRIGHT + (LEFTRIGHT * BOARD_WIDTH) + UPLEFT)


def askForPlayerMove(displayMode):
    """let the player select a color to paint the upper left tile"""
    while True:
        bext.fg('white')
        print('Choose one of ', end='')

        if displayMode == COLOR_MODE:
            bext.fg('red')
            print('(R)ed ', end='')
            bext.fg('green')
            print('(G)reen ', end='')
            bext.fg('blue')
            print('(B)lue ', end='')
            bext.fg('yellow')
            print('(Y)ellow ', end='')
            bext.fg('cyan')
            print('(C)yan ', end='')
            bext.fg('purple')
            print('(P)urple ', end='')
        elif displayMode == SHAPE_MODE:
            bext.fg('red')
            print('(Heart) ', end='')
            bext.fg('green')
            print('(T)riangle ', end='')
            bext.fg('blue')
            print('(D)iamond ', end='')
            bext.fg('yellow')
            print('(B)all ', end='')
            bext.fg('cyan')
            print('(C)lub ', end='')
            bext.fg('purple')
            print('(S)pade ', end='')
        bext.fg('white')
        print('or QUIT:')
        response = input('> ').upper()
        if response == 'QUIT':
            print('Thanks for playing!')
            sys.exit()
        if displayMode == COLOR_MODE and response in tuple('RGBYCP'):
            # return a tile type number based on the response
            return {'R': 0, 'G': 1, 'B': 2,
            'Y': 3, 'C': 4, 'P': 5}[response]
        if displayMode == SHAPE_MODE and response in tuple('HTDBCS'):
            # return a tile type number based on the response
            return {'H': 0, 'T': 1, 'D': 2,
            'B': 3, 'C': 4, 'S': 5}[response]


def changeTile(tileType, board, x, y, charToChange=None):
    """change the color/shape of a tile using the recursive flood fill
    algorithm"""
    if x == 0 and y == 0:
        charToChange = board[(x, y)]
        if tileType == charToChange:
            return  # base case: already is the same tile

    board[(x, y)] = tileType

    if x > 0 and board[(x - 1, y)] == charToChange:
        # Recursive Case: Change the left neighbor's tile:
        changeTile(tileType, board, x - 1, y, charToChange)
    if y > 0 and board[(x, y - 1)] == charToChange:
        # Recursive Case: Change the top neighbor's tile:
        changeTile(tileType, board, x, y - 1, charToChange)
    if x < BOARD_WIDTH - 1 and board[(x + 1, y)] == charToChange:
        # Recursive Case: Change the right neighbor's tile:
        changeTile(tileType, board, x + 1, y, charToChange)
    if y < BOARD_HEIGHT - 1 and board[(x, y + 1)] == charToChange:
        # Recursive Case: Change the bottom neighbor's tile:
        changeTile(tileType, board, x, y + 1, charToChange)


def hasWon(board):
    """Return True if the entire board is one color/shape."""
    tile = board[(0, 0)]

    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            if board[(x, y)] != tile:
                return False
    return True


# If this program was run (instead of imported), run the game:
if __name__ == '__main__':
    main()
