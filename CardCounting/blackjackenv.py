import random
import gym
import numpy as np
import math


PROBABILITIES = np.load("probabilities.npy")

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

def cmp(a, b):
    return float(a > b) - float(a < b)

class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value
        
    def __str__(self):
        return self.rank + " of " + self.suit.value

class Deck:
    def __init__(self, num=1):
        self.cards = []
        for i in range(num):
            for i in range(4):
                for rank, value in ranks.items():
                    self.cards.append(Card(rank, value))
                
    def shuffle(self):
        random.shuffle(self.cards)
        
    def deal(self):
        return self.cards.pop(0)
    
    def peek(self):
        if len(self.cards) > 0:
            return self.cards[0]
        
    def add_to_bottom(self, card):
        self.cards.append(card)

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
        temperature = math.floor(avg_value * 10)
        return temperature
            
    def __str__(self):
        result = ""
        for card in self.cards:
            result += str(card) + "\n"
        return result
    
    def __len__(self):
        return len(self.cards)

class GameState(tuple):
    def __init__(self, observation, env, done=False, reward=0):
        self.observation = observation
        self.env = env
        self.done = done
        self.reward = reward

    def take_action(self, action):
        observation, reward, terminated, truncated, _ = self.env.step(action)
        done = terminated or truncated
        return GameState(observation, self.env, done, reward)

    def is_terminal(self):
        return self.done

class ValueIterationAgent:
    def __init__(self, gamma=1.0, theta=0.0001):
        self.gamma = gamma
        self.theta = theta
        self.utilities = np.zeros((32, 32, 2, 2, 10))  # 32 for player sum, 32 for dealer card, 2 for usable ace, 2 for indicating turn, 10 for 'temperature'
        self.policy = np.zeros((32, 11, 2, 10), dtype=int)  # Policy: 0 (stick) or 1 (hit)

    def value_iteration(self, env):
        while True:
            delta = 0
            for player_sum in range(1, 32):
                for dealer_sum in range(1, 11):
                    for usable_ace in range(2):
                        for turn in range(2):
                            for temperature in range(0, 10):
                                v_old = self.utilities[player_sum, dealer_sum, usable_ace, turn, temperature]
                                v_new = self.evaluate_actions(env, player_sum, dealer_sum, usable_ace, turn, temperature)
                                self.utilities[player_sum, dealer_sum, usable_ace, turn, temperature] = v_new
                                delta = max(delta, abs(v_old - v_new))
            if delta < self.theta:
                break
        self.extract_policy(env)

    def evaluate_actions(self, env, player_sum, dealer_sum, usable_ace, turn, temperature):
        actions_values = np.zeros(env.action_space.n)
        for action in range(env.action_space.n):
            actions_values[action] = self.calculate_state_value(player_sum, dealer_sum, usable_ace, action, temperature)
            if turn == 1:
                return actions_values[0]
        return np.max(actions_values)

    def calculate_state_value(self, player_sum, dealer_sum, usable_ace, action, temperature):
        ev = 0
        probabilities = PROBABILITIES[temperature]
        if action == 0:  # stick
            for card in range(1, 11):
                card_value = card
                if card == 1:  # handle aces
                    # minimax
                    if self.utilities[player_sum - 1, dealer_sum + card - 1, usable_ace, 1, temperature] < self.utilities[player_sum - 1, dealer_sum + 11 - 1, usable_ace, 1, temperature]:
                        card_value = 11
                new_dealer_value = dealer_sum + card_value
                if new_dealer_value > 21:
                    ev += probabilities[card - 1] * 1
                elif new_dealer_value >= 17 and new_dealer_value > player_sum :
                    ev += probabilities[card - 1] * -1
                elif new_dealer_value >= 17 and new_dealer_value < player_sum :
                    ev += probabilities[card - 1] * 1
                else:
                    ev += probabilities[card - 1] * self.utilities[player_sum - 1, new_dealer_value - 1, usable_ace, 1, temperature]
        else:  # hit
            for card in range(1, 11):
                new_player_value = player_sum + card
                if new_player_value > 21:
                    ev += probabilities[card - 1] * -1
                else:
                    ev += self.utilities[new_player_value - 1, dealer_sum - 1, usable_ace, 0, temperature]
        return ev

    def extract_policy(self, env):
        print("Policy extracted")
        for player_sum in range(1, 32):
            for dealer_showing in range(1, 11):
                for usable_ace in range(2):
                        for temperature in range(0, 10):
                            action_values = np.zeros(env.action_space.n)
                            for action in range(env.action_space.n):
                                action_values[action] = self.calculate_state_value(player_sum, dealer_showing, usable_ace, action, temperature)
                            self.policy[player_sum - 1, dealer_showing - 1, usable_ace, temperature] = np.argmax(action_values)

for probability in PROBABILITIES:
    print(probability)
        
# Initialize the environment
env = gym.make('Blackjack-v1')

# Initialize the agent and perform value iteration
agent = ValueIterationAgent()
agent.value_iteration(env)

# Display the learned policy
print("Learned Policy:")
x_i= 1
for x in agent.policy:
    print("Player sum:" + str(x_i))
    y_i = 1
    for y in x:
        print("Dealer sum:" + str(y_i))
        print(y)
        y_i += 1
    x_i += 1

#np.save('learnedpolicy.npy', agent.policy)

# Display the learned policy
print("Learned Policy:")
for player_sum in range(1, 32):
    print(f"Player Sum: {player_sum}")
    for dealer_sum in range(1, 11):
        for usable_ace in range(0, 2):
            for temperature in range(0, 10):
                print(f"  Dealer Sum: {dealer_sum}; Usable Ace: {usable_ace}; Temperature{temperature} - Policy: {agent.policy[player_sum - 1, dealer_sum - 1]}")