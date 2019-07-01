#!/usr/bin/env python3

import sys
from shoe import Shoe
from players.player import Player
from players.dealer import Dealer

def test_split(run, player, dealer):
    if not run:
        return
    from players.hand import Hand
    player.hands[0] = Hand()
    player.hands[0].deal(6)
    player.hands[0].deal(6)

    dealer.hand = Hand()
    dealer.hand.deal(6)
    dealer.hand.deal(6)

if __name__ == '__main__':


    # Establish game
    iterations = 1
    num_decks = 1
    num_players = 1
    if len(sys.argv) is 4:
        iterations = int(sys.argv[1])
        num_decks = int(sys.argv[2])
        num_players = int(sys.argv[3])
    else:
        num_decks = int(input('Number of decks: '))
        num_players = int(input('Number of players: '))

    players = [Player() for _ in range(num_players)]
    dealer = Dealer()

    for i in range(iterations):
        shoe = Shoe(num_decks)


        # Deal hands
        for _ in range(2):
            for player in players:
                shoe.deal(player.hands[0])
            shoe.deal(dealer.hand)

        test_split(False, players[0], dealer)

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


        # print("--- Results ---")
        # print("Dealer hand:", dealer.hand)
        # print("Number of players:", num_players)
        # for p in range(num_players):
        #     print("Player {}:".format(p), players[p].hands, players[p].results)

        # Clear hands
        for player in players:
            player.clear_hand()
        dealer.clear_hand()

    # Compute final results
    for i in range(len(players)):
        player_wins = players[i].results.count('WIN')
        win_percent = player_wins / len(players[i].results)
        print("Player {}:".format(i), win_percent)
