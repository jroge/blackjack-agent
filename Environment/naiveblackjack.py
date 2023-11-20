from itertools import chain, combinations, product


class State(tuple):
    # A naive state is defined as a tuple (player_sum, player_isSoftHand, dealer_sum, dealer_isSoftHand)
    # Note we refer to this state as naive because it includes no information beyond the hand
    # of the player and that of the dealer
    # Access with the following command:
    # player_sum, player_isSoftHand, dealer_sum, dealer_isSoftHand = NaiveState
    def __new__(self, player_sum, player_isSoftHand, dealer_sum, dealer_isSoftHand):
        return tuple.__new__(
            State, (player_sum, player_isSoftHand, dealer_sum, dealer_isSoftHand)
        )


class Environment:
    def __all_states_and_actions(self):
        """
        Generate all possible states and actions in the environment.

        Returns:
        - states (list): List of all possible states in the environment.
        - actions (dict): Dictionary mapping states to possible actions in each state.
        """
        # Generate all possible combinations of player and dealer hand values
        possible_player_sums = range(2, 22)
        possible_dealer_sums = range(2, 12)  # Dealer upcard can be 2-11
        possible_softness = [False, True]  # Soft or hard hand

        # Directly convert the product to a list of states
        states = [
            State(player_sum, player_soft, dealer_sum, dealer_soft)
            for player_sum, dealer_sum, player_soft, dealer_soft in product(
                possible_player_sums,
                possible_dealer_sums,
                possible_softness,
                possible_softness,
            )
        ]

        # Define possible actions for each state (e.g., hit or stand)
        actions = {state: ["hit", "stand"] for state in states}

        return states, actions

    def __init__(self):
        self.all_states, self.all_states_actions = self.__all_states_and_actions()

    def available_actions(self, state):
        # Return a list of actions that is allowed in this case
        # Each action is a set of numbers.
        return self.all_states_actions[state]

    def all_transition_next(
        self, player_sum, player_soft, dealer_sum, dealer_soft, action_taken
    ):
        # Return a list of all possible next steps with their probability.
        # Input: Current state and an action (a subset of previous numbers)
        # Each next step is represented in tuple (state, probability of the state)
        # State is a tuple itself - (player_sum, player_isSoftHand, dealer_sum, dealer_isSoftHand)

        if action_taken == "hit":
            pass

        if action_taken == "stand":
            pass
