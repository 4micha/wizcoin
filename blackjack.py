"""Blackjack, by Al Sweigart
Auch bekannt als Zwanzig und Eins (21)
Tags: large, game, card game"""




import random, sys

# set up the constants:
HEARTS = chr(9829)  # Character 9829 is 'Herz'
DIAMONDS = chr(9830)  # ...
SPADES = chr(9824)  # 'Piek'
CLUBS = chr(9827)  # 'Kreuz'
# A list of chr codes is at https://inventwithpython.com/charactermap
BACKSIDE = 'backside'


def main():
    print("""Blackjack, by Al Sweigart
        Auch bekannt als 'Zwanzig und Eins'.
        Regeln:
        Versuche so nah wie möglich an 21 Punkt zu kommen,
        ohne darüber zu kommen.
        König, Dame und Bube sind 10 Punkte
        As kann als 1 oder 10 gezählt werden
        Karten von 2 bis 10 zählen als ihr angegebener Wert
        'H' (hit) für eine weitere Karte
        'S' (stand) für keine weitere Karte
        Vor der ersten weiteren Karte, besteht die Möglichkeit den Einsatz zu verdoppeln -
        'D' (double) es muss aber mindestens eine weitere Karte genommen werden.
        Bei unetschieden geht der Einsatz an den Spieler zurück.
        Der Dealer (Kartengeber) stoppt hitting bei 17 Punkten.""")
    money = 5000
    while True:  # Main game loop
        # check if the player has run out of money:
        if money <= 0:
            print('Du bist Bankrott!')
            print('Nur gut, dass das das kein echtes Geld gewesen ist.')
            print('Danke für`s spielen!')
            sys.exit()

        # let the player enter their bet for this round
        print('Geld: ', money)
        bet = getBet(money)

        # give the dealer and player two cards from the deck each:
        deck = getDeck()
        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]

        # handle player actions:
        print('Einsatz: ', bet)
        while True:  # keep looping until player stands or busts.
            displayHands(playerHand, dealerHand, False)
            print()

            # check if the player has bust
            if getHandValue(playerHand) > 21:
                break

            # get the player`s move, either H, S, or D:
            move = getMove(playerHand, money - bet)

            # handle the player actions:
            if move == 'D':
                # Player is doubling down, they can increase their bet:
                additionalBet = getBet(min(bet, (money - bet)))
                bet += additionalBet
                print('Der Einsatz ist erhöht um {}.'.format(bet))
                print('Einsatz: ', bet)

            if move in ('H', 'D'):
                # Hit or Double takes another card
                newCard = deck.pop()
                rank, suit = newCard
                print('Du hast ein {} {}.'.format(rank, suit))
                playerHand.append(newCard)

                if getHandValue(playerHand) > 21:
                    # the player has busted
                    continue
                    
            if move in ('S', 'D'):
                # Stand/doubling down stops the players turn
                break

        # handle the dealer's actions:
        if getHandValue(playerHand) <= 21:
            while getHandValue(dealerHand) < 17:
                # the dealer hits
                print('Der Dealer zieht...')
                dealerHand.append(deck.pop())
                displayHands(playerHand, dealerHand, False)

                if getHandValue(dealerHand) > 21:
                    break  # the dealer has busted
                    input('Drücke Enter für Neu...')
                    print('\n\n')

        # Show the final hands:
        displayHands(playerHand, dealerHand, True)

        playerValue = getHandValue(playerHand)
        dealerValue = getHandValue(dealerHand)
        # handle whether the player won, lost or tied
        if dealerValue > 21:
            print('Der Dealer hat verloren! Du hast gewonnen: {} $ !'.format(bet))
            money += bet
        elif (playerValue > 21) or (playerValue < dealerValue):
            print('Du hast verloren!')
            money -= bet
        elif playerValue > dealerValue:
            print('Du hast gewonnen! {} $ !'.format(bet))
            money += bet
        elif playerValue == dealerValue:
            print('Unentschieden, du bekommst den Einsatz zurück.')

        input('Drücke Enter für Neu...')
        print('\n\n')


def getBet(maxBet):
    """Ask the player how much they want to bet for this round."""
    while True:  # keep asking until they enter a valid amount
        print('Wie hoch ist dein Einsatz? (1-{}, or QUIT'.format(maxBet))
        bet = input('> ').upper().strip()
        if bet == 'QUIT':
            print('Danke für\'s spielen!')
            sys.exit()

        if not bet.isdecimal():
            continue

        bet = int(bet)
        if 1 <= bet <= maxBet:
            return bet  # player entered a valid bet


def getDeck():
    """Return a list of (rank, suit) ruples for all 52 cards."""
    deck =  []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))  # add the numbered cards
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))  # add the face and ace cards
    random.shuffle(deck)
    return deck


def displayHands(playerHand, dealerHand, showDealerHand):
    """Show the player's and dealer's cards. Hide the dealer's first
    card if showDealerHand is False."""
    print()
    if showDealerHand:
        print('DEALER: ', getHandValue(dealerHand))
        displayCards(dealerHand)
    else:
        print('DEALER: ???')
        # hide the dealer's first card
        displayCards([BACKSIDE] + dealerHand[1:])

    # show the player's cards:
    print('PLAYER: ', getHandValue(playerHand))
    displayCards(playerHand)


def getHandValue(cards):
    """Returns the value of the cards. Face card are worth 10, aces are
    worth 11 or 1 (this function picks the most suetable ace value)."""
    value = 0
    numberOfAces = 0

    # ad the value for the non-ace cards
    for card in cards:
        rank = card[0]  # card is a tuple like (rank, suit)
        if rank == 'A':
            numberOfAces += 1
        elif rank in ('J', 'Q', 'K'):
            value += 10
        else:
            value += int(rank)  # numbered cards are worth their number

    # Add the value for the aces:
    value += numberOfAces  # add 1 per ace
    for i in range(numberOfAces):
        # if another 10 can be added, do so
        if value + 10 <= 21:
            value += 10

    return value


def displayCards(cards):
    """Display all the cards in the cards list."""
    rows = ['', '', '', '', '']  # the text display on each row

    for i, card in enumerate(cards):
        rows[0] += ' ___ '  # top line of the card
        if card == BACKSIDE:
            # print a card's back
            rows[1] += '|## |'
            rows[2] += '|###|'
            rows[3] += '| ##|'
        else:
            # print the card's front
            rank, suit = card  # the card is a tuple data structure
            rows[1] += '|{} |'.format(rank.ljust(2))
            rows[2] += '| {} |'.format(suit)
            rows[3] += '|_{}|'.format(rank.rjust(2, '_'))

    # print each row in the screen
    for row in rows:
        print(row)


def getMove(playerHand, money):
    """Asks the player for their move, and returns 'H' for hit, 'S' for
    stand, and 'D' for double down."""
    while True:  # keep looping until the player enters a correct move
        # determine what moves the player can make
        moves = ['(H)it/ ziehen', '(S)tand/ halten']

        # the player can double down on their first move, which we can
        # tell because they'll have exactly two cards
        if len(playerHand)  == 2 and money > 0:
            moves.append('(D)ouble down/ verdoppeln')

        # get the players move
        movePrompt = ', '.join(moves) + '> '
        move = input(movePrompt).upper()
        if move in ('H', 'S'):
            return move  # player has entered a valid move
        if move == 'D' and '(D)ouble down/ verdoppeln' in moves:
            return move  # player has entered a valid move


# if the program is run (instead of imported), run the game:
if __name__ == '__main__':
    main()