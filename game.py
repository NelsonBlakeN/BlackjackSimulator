#!/usr/bin/env python3

import sys
from helpers import Shoe, Player, Dealer, Hand

#TODO: Implement split logic
#TODO: Calculate odds if one player is using the strategy while others are not OR while all players use the strategy (comparison)

if __name__ == '__main__':
    # Establish game
    num_decks = 1
    num_players = 1
    if len(sys.argv) is 3:
        num_decks = int(sys.argv[1])
        num_players = int(sys.argv[2])
    else:
        num_decks = int(input('Number of decks: '))
        num_players = int(input('Number of players: '))

    shoe = Shoe(num_decks)

    players = [Player() for _ in range(num_players)]
    dealer = Dealer()

    # Deal hands
    for _ in range(2):
        for player in players:
            shoe.deal(player.hands[0])
        shoe.deal(dealer.hand)

    dealer.show_card = dealer.hand[1]

    # Check for dealer blackjack
    if dealer.total is 21:
        for player in players:
            for hand in player.hands:
                if hand.total is 21:
                    player.results.append("PUSH")
                else:
                    player.results.append("LOSE")
    else:
        # Players play
        for player in players:
            player.play(shoe, dealer.show_card)

        # Dealer plays
        dealer.play(shoe)

        # Calculate results
        for player in players:
            for hand in player.hands:
                if hand.total <= 21 and (dealer.total > 21 or hand.total > dealer.total):
                    player.results.append('WIN')
                elif hand.total > 21 or hand.total < dealer.total:
                    player.results.append('LOSE')
                else:
                    player.results.append('PUSH')

    print("--- Results ---")
    print("Dealer hand:", dealer.hand)
    print("Number of players:", num_players)
    for p in range(num_players):
        print("Player {}:".format(p), players[p].results)
