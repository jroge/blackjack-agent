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
#np.save('probabilities.npy', probabilities)

# Load probabilities from npy file
loaded_probabilities = np.load('probabilities.npy')