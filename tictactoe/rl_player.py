import pickle
import pprint

from tictactoe.player import Player


class RLPlayer(Player):
    def __init__(self, symbol, alpha):
        super().__init__(symbol)
        self._alpha = alpha
        self._values = {}
        self._last_state = None

    def get_input(self, board):
        state = self._get_board_state(board)
        action_space = self._get_action_space(state)

        use_greedy_action = True  # TODO set epsilon
        if use_greedy_action:
            action = self._get_greedy_action(action_space, state)
        else:
            action = action_space[0]  # TODO explore
        line = action//3
        column = action % 3
        return line, column

    def process(self, board, current_player):
        state = self._get_board_state(board)
        winner = self._check_winner(state)
        if winner != 1 or current_player is self:
            self._update_last_action_value(state)
            self._last_state = state

    def _get_board_state(self, board):
        return tuple([
            1 if element == self._symbol else
            0 if element == ' ' else
            -1
            for line in board for element in line
        ])

    def _update_last_action_value(self, state):
        if self._last_state is None:
            return
        last_state_value = self._get_state_value(self._last_state)
        current_state_value = self._get_state_value(state)
        updated_value = last_state_value + self._alpha*(current_state_value-last_state_value)
        self._values[self._last_state] = updated_value

    def _get_action_space(self, state):
        action_space = [
            idx for idx, element in enumerate(state) if element == 0
        ]
        action_space.reverse()
        return action_space

    def _get_greedy_action(self, action_space, state):
        greedy_action = None
        greddy_action_value = 0
        for action in action_space:
            new_state = self._get_action_state(action, state)
            value = self._get_state_value(new_state)
            if value >= greddy_action_value:
                greedy_action = action
                greddy_action_value = value
        return greedy_action

    def _get_action_state(self, action, state):
        new_state = list(state)
        new_state[action] = 1
        return tuple(new_state)

    def _get_state_value(self, state):
        if state in self._values:
            return self._values[state]

        winner = self._check_winner(state)
        if winner == 1:
            return self._values.setdefault(state, 1)
        if winner == -1:
            return self._values.setdefault(state, 0)
        return self._values.setdefault(state, 0.5)

    def _check_winner(self, state):
        for i in range(3):
            line_value = sum(state[3*i:3*(i+1)])
            if abs(line_value) == 3:
                return line_value//abs(line_value)

            row_value = sum(state[i::3])
            if abs(row_value) == 3:
                return row_value//abs(row_value)

        diagonal_value = sum(state[::4])
        if abs(diagonal_value) == 3:
            return diagonal_value//abs(diagonal_value)

        inverse_diagonal_value = sum(state[2:7:2])
        if abs(inverse_diagonal_value) == 3:
            return inverse_diagonal_value//abs(inverse_diagonal_value)

        if len(self._get_action_space(state)) == 0:
            return -1

        return 0

    def print_values(self):
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(self._values)

    def save_values(self, filename):
        with open(filename, 'wb') as f:
            pickler = pickle.Pickler(f)
            pickler.dump(self._values)

    def load_values(self, filename):
        with open(filename, 'rb') as f:
            unpickler = pickle.Unpickler(f)
            self._values = unpickler.load()
