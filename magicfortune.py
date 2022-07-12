"""Magic Fortune Ball, by Al Sweigart
Ask a yes/no question about your future. Inspired by the Magic 8 Ball.

Tags: tiny, beginner, humor"""

import random, time


def slowSpacePrint(text, interval=0.1):
    """Slowly display text with spaces in between each letter and
    lowecase letter i's."""
    for character in text:
        if character == 'I':
            # I's are displayed in lowercase for style
            print('i ', end='', flush=True)
        else:
            # all other characters are displayed normally
            print(character + ' ', end='', flush=True)
        time.sleep(interval)
    print()
    print()


# prompt for a question
slowSpacePrint('MAGIC FORTUNE BALL, BY AL SWEIGART')
time.sleep(0.5)
slowSpacePrint('ASK ME YOUR YES/NO QUESTION.')
input('> ')

# display a brief reply
replies = [
    'LET ME THINK ON THIS...',
    'AN INTERESTING QUESTION...',
    'HMMM... ARE YOU SURE YOU WANT TO KNOW..?',
    'DO YOU THINK SOME THINGS ARE BEST LEFT UNKNOWN..?',
    'I MIGHT TELL YOU, BUT YOU MIGHT NOT LIKE THE ANSWERE...'
    'YES... NO... MAYBE... I WILL THINK ON IT...',
    'AND WHAT WILL YOU DO WHEN YOU SEE THE ANSWERE? WE SHALL SEE...',
    'I SHALL CONSULT MY VISIONS...',
    'YOU MAY WANT TO SIT DOWN FOR THIS...',
]
slowSpacePrint(random.choice(replies))

# dramatic pause
slowSpacePrint('.' * random.randint(4, 12), 0.7)

# give the answere
slowSpacePrint('I HAVE AN ANSWER...', 0.2)
time.sleep(1)
answer = [
    'YES, FOR SURE.',
    'MY ANSWERE IS NO',
    'ASK ME LATER',
    'I AM PROGRAMMED TO SAY YES',
    'THE STARS SAY YES, BUT I SAY NO',
    'I DUNNO MAYBE',
    'FOCUS AND ASK ONCE MORE',
    'DOUBTFUL, VERY DOUBTFUL',
    'AFFIRMATIVE',
    'YES, THOUGH YOU MAY NOT LIKE IT',
    'NO, BUT YOU MAY WISH IT WAS SO',
]
slowSpacePrint(random.choice(answer), 0.5)
