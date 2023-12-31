from CardGame import Deck, Hand, Card, Suit
import PlayPhase
from CribbageGui import CribbageGUI

class Player:
    hand: Hand
    points: int
    isDealer: bool

    def __init__(self, isDealer: bool) -> None:
        self.points = 0
        self.isDealer = isDealer
        self.hand = Hand()

    def discard_card(self):
        # Placeholder implementation, actual player interaction will be here

        if self.hand.cards:
            return self.hand.cards.pop(0)
        else:
            raise Exception("No cards to discard")
        
    def has_card_of_suit(self, suit):
        return any(card.suit == suit for card in self.hand.cards)

class Round:
    dealer: Player
    playerTwo: Player
    deck: Deck
    crib: Hand
    starter: Card
    GUI: CribbageGUI


    def __init__(self, player_one: Player, player_two: Player) -> None:
        if player_one.isDealer and player_two.isDealer:
            raise Exception("Both players cannot be dealers.")
        elif not player_one.isDealer and not player_two.isDealer:
            raise Exception("One player must be the dealer.")

        self.dealer = player_one if player_one.isDealer else player_two
        self.non_dealer = player_two if player_one.isDealer else player_one

        self.deck = Deck(shuffled=True)
        self.crib = Hand()
        self.deal_hands()

    def deal_hands(self):
        # Deal 6 cards to each player
        for _ in range(6):
            self.dealer.hand.pickup(self.deck.draw_card())
            self.non_dealer.hand.pickup(self.deck.draw_card())

    def discard_to_crib(self):
        # Each player discards two cards to the crib
        for _ in range(2):
            self.crib.pickup(self.dealer.discard_card())  # Assuming discard_card method in Player class
            self.crib.pickup(self.non_dealer.discard_card())

    def play(self):
        self.discard_to_crib()

        self.starter = self.deck.draw_card()

        # 'His heels' rule
        if self.starter.value == 11: 
            if self.dealer.has_card_of_suit(self.starter.suit):
                self.dealer.points += 2


class CribbageGame:
    def __init__(self, player_one: Player, player_two: Player):
        self.player_one = player_one
        self.player_two = player_two

    def start(self):
        while True:
            round = Round(self.player_one, self.player_two)
            continue_game = round.play()
            if not continue_game:
                break
            # Additional logic to switch dealer, reset states, etc.

        # Determine and announce the winner




# Game initialization
player_one = Player(True)
player_two = Player(False)
game = CribbageGame(player_one, player_two)
game.start()




