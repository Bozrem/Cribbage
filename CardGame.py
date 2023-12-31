import random
import itertools
from collections import Counter


class Suit:
    # 1      2     3      4
    # Spade, Club, Heart, Diamond

    suitID: int

    def __init__(self, numericalsuit: int) -> None:
        if 0 > numericalsuit or numericalsuit > 4:
            raise Exception(f"Given integer {numericalsuit} is not in valid range 1 to 4")
        self.suitID = numericalsuit

    @classmethod
    def fromString(cls, suitName: str):
        suitName = suitName.lower()
        if suitName == "spade":
            suitID = 1
        elif suitName == "club":
            suitID = 2
        elif suitName == "heart":
            suitID = 3
        elif suitName == "diamond":
            suitID = 4
        else:
            raise Exception(f"String \"{suitName}\" is not a valid suit")
        return cls(suitID)
    
    def __str__(self) -> str:
        if self.suitID == 1:
            return "spade"
        elif self.suitID == 2:
            return "club"
        elif self.suitID == 3:
            return "heart"
        elif self.suitID == 4:
            return "diamond"
        return "Invalid value"
    
    def __eq__(self, __value: object) -> bool:
        return self.suitID == __value.suitID

class Card:

    suit: Suit
    value: int

    def __init__(self, suit: Suit, value: int) -> None:
        self.suit = suit
        if 1 > value or value > 13:
            raise ValueError(f"Invalid card value; {value} is not between 1 and 13")
        self.value = value
    
    def getCribbageValue(self) -> int:
        return min(10, self.value)
    
    def __str__(self) -> str:
        return f"{self.value} of {self.suit}s"
    
    def __eq__(self, __value: object) -> bool:
        return self.suit == __value.suit and self.value == __value.value

class Deck:
    cards: [Card]

    def __init__(self, shuffled: bool) -> None:
        self.cards = []
        for suit_id in range(1, 5):  # Suits are 1 to 4
            for value in range(1, 14):  # Card values are 1 to 13
                self.cards.append(Card(Suit(suit_id), value))
        
        if shuffled:
            random.shuffle(self.cards)

    def draw_card(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            raise Exception("No more cards in the deck")

    def __str__(self):
        return ', '.join([str(card) for card in self.cards])
    
class Hand:
    cards: [Card]
    
    def __init__(self) -> None:
        self.cards = []
    
    def pickup(self, cards):
        if isinstance(cards, list):
            self.cards.extend(cards)
            return
        self.cards.append(cards)
    
    def __str__(self):
        return ', '.join([str(card) for card in self.cards])

    def __eq__(self, other) -> bool:
        return self.suitID == other.suitID
    
    # Scoring functions

    def get_total_score(self, starter: Card) -> int:
        total = 0
        total += self.score_nob(starter)
        # For the rest, a starter is just included as part of the hand
        hand_with_starter: Hand = self
        hand_with_starter.pickup(starter)
        total += hand_with_starter.score_15s()
        total += hand_with_starter.score_pairs()
        total += hand_with_starter.score_flush()
        total += hand_with_starter.score_runs()

        return total

    def score_nob(self, starter: Card):
        total = 0
        if starter.value == 11: return 0
        for card in self.cards:
            if card.value == 11 and card.suit == starter.suit: return 1
        return 0

    def score_15s(self):
        total_score = 0
        for r in range(2, 6):  # Combinations of 2, 3, 4, and 5 cards
            for combo in itertools.combinations(self.cards, r):
                if sum(card.getCribbageValue() for card in combo) == 15:
                    total_score += 2  # Each valid combination scores 2 points
        return total_score
    
    def score_pairs(self):
        total_score = 0
        for combo in itertools.combinations(self.cards, 2):
            if combo[0].value == combo[1].value:
                total_score += 2  # Each pair is worth 2 points
        return total_score
    
    def score_runs(self):
        value_counts = Counter(card.value for card in self.cards)
        longest_run_length, run_combinations = self.find_longest_run(value_counts)

        total_score = 0
        for combo in run_combinations:
            combo_score = longest_run_length
            for value in combo:
                combo_score *= value_counts[value]
            total_score += combo_score

        return total_score

    def find_longest_run(self, value_counts):
        for run_length in range(5, 2, -1):  # Check for runs of length 5, 4, and 3
            for combo in itertools.combinations(sorted(value_counts.keys()), run_length):
                if self.is_consecutive(combo):
                    return run_length, [combo]
        return 0, []

    def is_consecutive(self, combo):
        return all(combo[i] + 1 == combo[i + 1] for i in range(len(combo) - 1))
    
    def score_flush(self):
        suit_count = {}
        for card in self.cards:
            suit_id = card.suit.suitID  # Use suitID instead of the Suit object
            suit_count[suit_id] = suit_count.get(suit_id, 0) + 1

        for count in suit_count.values():
            if count >= 4:
                return count
        return 0
    


    