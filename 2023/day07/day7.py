## For part 1
#label_values = {"A":14, "K":13, "Q":12, "J":11, "T": 10, "9": 9, "8":8, "7":7, "6":6, "5":5, "4":4, "3":3, "2":2}
## For part 2
label_values = {"A":14, "K":13, "Q":12, "J":1, "T": 10, "9": 9, "8":8, "7":7, "6":6, "5":5, "4":4, "3":3, "2":2}

class Hand():
    def __init__(self, cards, bid):
        self.h = list(cards)
        self.bid = bid
        self.counts = {}
        for card in cards:
            self.counts[card] = self.counts.get(card, 0) + 1

    def __repr__(self):
        return "".join(self.h)

    def __lt__(self, other):
        if other._is_5_of_a_kind():
            if self._is_5_of_a_kind():
                return self._first_label_less(other)
            return True

        if self._is_5_of_a_kind():
            return False

        if other._is_4_of_a_kind():
            if self._is_4_of_a_kind():
                return self._first_label_less(other)
            return True
        if self._is_4_of_a_kind():
            return False

        if other._is_full_house():
            if self._is_full_house():
                return self._first_label_less(other)
            return True
        if self._is_full_house():
            return False

        if other._is_3_of_a_kind():
            if self._is_3_of_a_kind():
                return self._first_label_less(other)
            return True
        if self._is_3_of_a_kind():
            return False
        
        if other._is_2_pairs():
            if self._is_2_pairs():
                return self._first_label_less(other)
            return True
        if self._is_2_pairs():
            return False
        
        if other._is_pair():
            if self._is_pair():
                return self._first_label_less(other)
            return True
        if self._is_pair():
            return False

        return self._first_label_less(other)

    def _first_label_less(self, other):
        for i in range(len(self.h)):
            if self.h[i] != other.h[i]:
                return label_values[self.h[i]] < label_values[other.h[i]]
        return False

    def _is_5_of_a_kind(self): 
        return len(self.counts) == 1

    def _is_4_of_a_kind(self):
        for c in self.counts.values():
            if c == 4:
                return True
        return False
    
    def _is_3_of_a_kind(self):
        for c in self.counts.values():
            if c == 3:
                return True
        return False

    def _is_full_house(self):
        return self._is_3_of_a_kind() and len(self.counts) == 2

    def _is_pair(self):
        return self._count_pairs() > 0

    def _is_2_pairs(self):
        return self._count_pairs() == 2

    def _count_pairs(self): 
        n = 0
        for c in self.counts.values():
            if c == 2:
                n += 1
        return n


def part1():
    winnings = 0
    for i, hand in enumerate(sorted(hands)):
        winnings += (i+1) * hand.bid
    return winnings


def find_strongest_version(hand):
    for i in range(len(hand.h)):
        if hand.h[i] == "J":
            variants = []
            for c in label_values:
                if c == "J": 
                    continue
                new_cards = hand.h.copy()
                new_cards[i] = c
                new_hand = Hand(new_cards, hand.bid)
                new_hand = find_strongest_version(new_hand)
                variants.append(new_hand)
            return sorted(variants)[-1]
    return hand


def part2():
    strongest_hands = []
    for hand in hands:
        hand = find_strongest_version(hand)
        strongest_hands.append(hand)

    winnings = 0
    for i, hand in enumerate(sorted(strongest_hands)):
        winnings += (i+1) * hand.bid
    return winnings


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = [l.strip().split() for l in f.readlines()]
        hands = [Hand(l[0], int(l[1])) for l in lines]
   
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
