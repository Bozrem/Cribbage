import unittest
from CardGame import Card, Suit, Deck, Hand
from CribbageGame import Player

class SuitTest(unittest.TestCase):

    def test_initialization_valid(self):
        suit = Suit(1)
        self.assertEqual(suit.suitID, 1)

    def test_initialization_invalid(self):
        with self.assertRaises(Exception):
            Suit(5)

    def test_from_string_valid(self):
        suit = Suit.fromString("heart")
        self.assertEqual(suit.suitID, 3)

    def test_from_string_invalid(self):
        with self.assertRaises(Exception):
            Suit.fromString("invalid")

    def test_string_representation(self):
        suit = Suit(2)
        self.assertEqual(str(suit), "club")

class CardTest(unittest.TestCase):
    def test_card_creation(self):
        card = Card("Hearts", 10)
        self.assertEqual(card.suit, "Hearts")
        self.assertEqual(card.value, 10)

    def test_invalid_card_value(self):
        with self.assertRaises(ValueError):
            Card("Hearts", 15)

class DeckTest(unittest.TestCase):

    def test_deck_initialization(self):
        deck = Deck(False)
        self.assertEqual(len(deck.cards), 52)  # A deck should have 52 cards

    def test_deck_shuffling(self):
        deck1 = Deck(False)
        deck2 = Deck(True)
        self.assertNotEqual(deck1.cards, deck2.cards)  # Shuffled deck should be different

    def test_draw_card(self):
        deck = Deck(False)
        card = deck.draw_card()
        self.assertEqual(len(deck.cards), 51)  # One card should be removed
        self.assertIsNotNone(card)  # Drawn card should not be None

    def test_draw_from_empty_deck(self):
        deck = Deck(False)
        for _ in range(52):
            deck.draw_card()
        with self.assertRaises(Exception):
            deck.draw_card()

class HandTest(unittest.TestCase):

    def test_hand_initialization(self):
        hand = Hand()
        self.assertEqual(len(hand.cards), 0)

    def test_pickup_card(self):
        hand = Hand()
        card = Card(Suit(1), 5)
        hand.pickup(card)
        self.assertEqual(len(hand.cards), 1)  # Hand should have one card after pickup
        self.assertIn(card, hand.cards)  # The picked-up card should be in the hand

class HandScoringTest(unittest.TestCase):
    def test_score_15s(self):
        hand = Hand()
        hand.pickup([Card(Suit(1), 9), Card(Suit(2), 9), Card(Suit(3), 9), Card(Suit(4), 9)]) # 9 of all Suits
        self.assertEqual(hand.score_15s(), 0)  # No combinations sum to 15

        hand = Hand()
        hand.pickup([Card(Suit(1), 5), Card(Suit(2), 10)]) # 5 of Spades and 10 of Clubs
        self.assertEqual(hand.score_15s(), 2)  # One combination sums to 15

        hand = Hand()
        hand.pickup([Card(Suit(1), 5), Card(Suit(2), 5), Card(Suit(3), 5), Card(Suit(4), 10)])  
        self.assertEqual(hand.score_15s(), 8) # 3 combinations of 5 and 10, 1 combination of fives
    
    def test_score_pairs(self):
        hand = Hand()
        hand.pickup([Card(Suit(1), 9), Card(Suit(2), 7), Card(Suit(3), 8), Card(Suit(4), 6)])  # No pairs
        self.assertEqual(hand.score_pairs(), 0)  # No pairs

        hand = Hand()
        hand.pickup([Card(Suit(1), 5), Card(Suit(2), 5)])  # One pair of 5s
        self.assertEqual(hand.score_pairs(), 2)  # One pair

        hand = Hand()
        hand.pickup([Card(Suit(1), 4), Card(Suit(2), 4), Card(Suit(3), 4)])  # Triple of 4s
        self.assertEqual(hand.score_pairs(), 6)  # Triple counts as three pairs

        hand = Hand()
        hand.pickup([Card(Suit(1), 11), Card(Suit(2), 11), Card(Suit(3), 11), Card(Suit(4), 11)])  # Four of a kind (Jacks)
        self.assertEqual(hand.score_pairs(), 12) # Four of a kind counts as six pairs

    def test_score_nob(self):
        hand = Hand()
        starter = Card(Suit(1), 11) # Jack of spades
        hand.pickup([Card(Suit(1), 9), Card(Suit(2), 9), Card(Suit(3), 9), Card(Suit(4), 9)])
        self.assertEqual(hand.score_nob(starter), 0) # Would've got 'his heels' already

        hand = Hand()
        starter = Card(Suit(1), 9) # 9 of spades
        hand.pickup([Card(Suit(1), 11), Card(Suit(2), 9), Card(Suit(3), 9), Card(Suit(4), 9)])
        self.assertEqual(hand.score_nob(starter), 1) # Jack of spades with 9 of Spades

        hand = Hand()
        starter = Card(Suit(1), 13) # King of spades
        hand.pickup([Card(Suit(1), 9), Card(Suit(2), 9), Card(Suit(3), 9), Card(Suit(4), 9)]) # All 9s
        self.assertEqual(hand.score_nob(starter), 0) # No jack to make a nob

    def test_score_flush(self):
        hand = Hand()
        hand.pickup([Card(Suit(1), 5), Card(Suit(1), 6), Card(Suit(1), 7), Card(Suit(1), 8)])
        self.assertEqual(hand.score_flush(), 4)  # Flush of 4 cards

        hand = Hand()
        hand.pickup([Card(Suit(1), 9), Card(Suit(2), 9), Card(Suit(1), 10), Card(Suit(1), 11)])
        self.assertEqual(hand.score_flush(), 0)  # No flush

    def test_score_runs(self):
        hand = Hand()
        hand.pickup([Card(Suit(1), 5), Card(Suit(2), 6), Card(Suit(3), 7)])
        self.assertEqual(hand.score_runs(), 3)  # Run of 3

        hand = Hand()
        hand.pickup([Card(Suit(1), 5), Card(Suit(2), 6), Card(Suit(3), 7), Card(Suit(1), 8), Card(Suit(3), 9)])
        self.assertEqual(hand.score_runs(), 5)  # Run of 5

        hand = Hand()
        hand.pickup([Card(Suit(1), 5), Card(Suit(2), 6), Card(Suit(3), 6), Card(Suit(1), 7), Card(Suit(3), 7)])
        self.assertEqual(hand.score_runs(), 12)  # 4 Runs of 3

        hand = Hand()
        hand.pickup([Card(Suit(1), 1), Card(Suit(2), 3), Card(Suit(3), 5), Card(Suit(4), 7), Card(Suit(1), 10)])
        self.assertEqual(hand.score_runs(), 0)  # No run

    def test_total_score(self):
        hand = Hand()
        hand.pickup([Card(Suit(1), 2), Card(Suit(2), 3), Card(Suit(3), 4)])
        starter = Card(Suit(4), 5)
        self.assertEqual(hand.get_total_score(starter), 4)  # Run of 4

        hand = Hand()
        hand.pickup([Card(Suit(1), 5), Card(Suit(2), 5), Card(Suit(3), 10)]) 
        starter = Card(Suit(4), 9)
        self.assertEqual(hand.get_total_score(starter), 6)  # Pair and 2 15's

        hand = Hand()
        hand.pickup([Card(Suit(1), 2), Card(Suit(1), 3), Card(Suit(1), 4), Card(Suit(1), 5)])
        starter = Card(Suit(2), 10)
        self.assertEqual(hand.get_total_score(starter), 12)  # Flush of 4, Run of 4, 2 sets of 15 (10+5, 10+2+3)


class PlayerTest(unittest.TestCase):

    def setUp(self):
        self.player = Player(isDealer=False)
        self.card1 = Card(Suit(1), 5)  # Example card
        self.card2 = Card(Suit(2), 10) # Another example card
        self.player.hand.pickup(self.card1)
        self.player.hand.pickup(self.card2)

    def test_initialization(self):
        self.assertEqual(self.player.points, 0)
        self.assertFalse(self.player.isDealer)
        self.assertIsNotNone(self.player.hand)

    def test_discard_card(self):
        discarded_card = self.player.discard_card()
        self.assertEqual(discarded_card, self.card1)
        self.assertEqual(len(self.player.hand.cards), 1)

    def test_discard_from_empty_hand(self):
        self.player.hand.cards.clear()  # Clear the hand
        with self.assertRaises(Exception):
            self.player.discard_card()

    def test_has_card_of_suit(self):
        self.assertTrue(self.player.has_card_of_suit(Suit(1)))  # Suit of card1
        self.assertFalse(self.player.has_card_of_suit(Suit(3))) # Non-existent suit




if __name__ == '__main__':
    unittest.main()
