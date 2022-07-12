"""Hex Grid, by Al Sweigart
Displays a simple tessellation of hexagon grid
Tags: tiny, beginner, artistic"""


# set up the constants

X_REPEAT = 19 * 4  # horizontal
Y_REPEAT = 12 * 3  # vertical

for y in range(Y_REPEAT):
    for x in range(X_REPEAT):
        print(r'/ \_', end='')
    print()

    for x in range(X_REPEAT):
        print(r'\_/ ', end='')
    print()
