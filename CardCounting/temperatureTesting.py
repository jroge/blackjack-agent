import random
import gym
import numpy as np
import math

ranks = {
    "two" : 2,
    "three" : 3,
    "four" : 4,
    "five" : 5,
    "six" : 6,
    "seven" : 7,
    "eight" : 8,
    "nine" : 9,
    "ten" : 10,
    "jack" : 10,
    "queen" : 10,
    "king" : 10,
    "ace" : (1, 11)
}

class Card:
    def __init__(self, value):
        self.value = value
        
class Deck:
    def __init__(self, number_decks=1):
        self.cards = []
        for i in range(number_decks):
            for i in range(4):
                for rank, value in ranks.items():
                    self.cards.append(Card(value))
                
    def shuffle(self):
        random.shuffle(self.cards)
        
    def deal(self):
        return self.cards.pop(0)
    
    def peek(self):
        if len(self.cards) > 0:
            return self.cards[0]
        
    def add_to_bottom(self, card):
        self.cards.append(card)

    """
    In 10000 simulations, Max achieved: 7.729166666666667, Min achieved: 6.0894308943089435
    """
    def scale_value(self, value):
        scaled_value = ((value - 6.0) / (7.8 - 6.0)) * (9)
        return scaled_value

    def calc_temperature(self):
        deck_value = 0
        for card in self.cards:
            if isinstance(card.value, tuple):
                # Treat ace as 1 in temperature calculations
                value, _ = card.value
            else:
                 # Take the value as is
                value = card.value
            deck_value += value
        avg_value = deck_value / len(self)
        temperature = math.floor(self.scale_value(avg_value))
        return temperature
            
    def __str__(self):
        result = ""
        for card in self.cards:
            result += str(card) + "\n"
        return result
    
    def __len__(self):
        return len(self.cards)

num_simulations = 1000000000
draws_between_shuffle = math.floor(6 * 52 * 0.7)

deck = Deck(number_decks=6)
deck.shuffle()

implied_odds = {}
count = np.zeros((10, 10))
index = 0
prints = 0
for i in range(num_simulations):
    if i == (num_simulations / 100) * (1 + prints):
        print(i)
        prints += 1
    avg_value = deck.calc_temperature()
    card = deck.deal()
    if isinstance(card.value, tuple):
        # Treat ace as 1 in temperature calculations
        value, _ = card.value
    else:
        # Take the value as is
        value = card.value
    count[avg_value - 1][value - 1] += 1
    index += 1
    if index > draws_between_shuffle:
        deck = Deck(number_decks=6)
        deck.shuffle()
        index = 0

probabilities = np.zeros((10, 10))

for i in range(0, 10):
    total = 0
    for j in range(0, 10):
        total += count[i][j]
    for j in range(0, 10):
        probabilities[i][j] = count[i][j] / total

for i in range(0, 10):
    print(f"Implied odds for each card at temperature {i} after {num_simulations} simulations:")
    sum = 0
    for j in range(0, 10):
        print(f"Card value {j+1}: {probabilities[i][j]:.2%}")
        sum += probabilities[i][j]
    print(f"Law of total probability: {sum} (Should equal 1)")

# Save probabilities to an npy file
# Got deleted but here they are
"""[0.08589279 0.08428358 0.08270182 0.08107326 0.07947306 0.07786539
 0.07624694 0.07458229 0.07295212 0.28492874]
[0.07798619 0.07777157 0.07757034 0.07737118 0.07720059 0.0769936
 0.07681823 0.0766466  0.07646184 0.30517987]
[0.0711134  0.07220703 0.07324867 0.07433814 0.07536074 0.07643068
 0.07741971 0.07846479 0.07946522 0.32195161]
[0.06264135 0.06521242 0.06783794 0.07039011 0.07300846 0.07546747
 0.07813063 0.08064167 0.08333135 0.34333859]
[0.05492609 0.05866563 0.06241861 0.0664246  0.0703238  0.07438929
 0.07876241 0.08263526 0.08690159 0.3645527 ]
[0.04729923 0.05229569 0.05699662 0.06245117 0.06741992 0.0730795
 0.07827176 0.08449656 0.09123301 0.38645654]
[0.06242049 0.06520192 0.06559003 0.06774618 0.06867332 0.07443024
 0.07527114 0.08053214 0.0840251  0.35610945]
[0.11136802 0.10441322 0.09907285 0.09171216 0.08652684 0.07962221
 0.07248954 0.06736351 0.06265249 0.22477916]
[0.10392516 0.09868372 0.09321033 0.0887612  0.0838394  0.07905484
 0.07428343 0.06953439 0.06506728 0.24364025]
[0.09465675 0.09127196 0.08812075 0.084798   0.08170729 0.07859511
 0.07534853 0.07221468 0.06911658 0.26417035]"""
#np.save('probabilities.npy', probabilities)

# Load probabilities from npy file
loaded_probabilities = np.load('probabilities.npy')