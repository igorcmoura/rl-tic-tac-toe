from tictactoe import screen


class Game:
    def __init__(self, player1, player2):
        self._player1 = player1
        self._player2 = player2
        self._victories = {
            player1: 0,
            player2: 0,
        }
        self.reset()

    def reset(self):
        self._board = [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' '],
        ]
        self._winner = None
        self._current_player_1 = True
        self._win_accounted = False

    @property
    def board(self):
        return tuple([tuple(line) for line in self._board])

    def get_input(self):
        current_player = self._player1 if self._current_player_1 else self._player2
        line, column = current_player.get_input(self.board)
        is_valid_play, non_valid_reason = self._is_valid_play(line, column)
        while not is_valid_play:
            print(non_valid_reason)
            line, column = current_player.get_input(self.board)
            is_valid_play, non_valid_reason = self._is_valid_play(line, column)

        self._board[line][column] = current_player.symbol

    def process(self):
        current_player = self._player1 if self._current_player_1 else self._player2
        self._player1.process(self.board, current_player)
        self._player2.process(self.board, current_player)

        self._current_player_1 = not self._current_player_1

    def render(self):
        screen.clear()
        pl1_symbol = self._player1.symbol
        pl1_victories = self._victories[self._player1]
        pl2_symbol = self._player2.symbol
        pl2_victories = self._victories[self._player2]
        print(f'{pl1_symbol} {pl1_victories}-{pl2_victories} {pl2_symbol}')
        print()

        board = [
            [
                element if element != ' ' else str((line_idx*3)+(row_idx+1))
                for row_idx, element in enumerate(line)
            ]
            for line_idx, line in enumerate(self.board)
        ]
        print('\n-----\n'.join(['|'.join(line) for line in board]))
        if self.ended():
            if self._winner is not None:
                symbol = self._winner.symbol
                print(f'Winner: {symbol}')
            else:
                print('Draw!')

    def ended(self):
        if self._check_winning_condition(self._player1.symbol):
            self._winner = self._player1
        elif self._check_winning_condition(self._player2.symbol):
            self._winner = self._player2

        if self._winner is not None:
            if not self._win_accounted:
                self._victories[self._winner] += 1
                self._win_accounted = True
            return True

        return not any([space == ' ' for line in self.board for space in line])

    def _is_valid_play(self, line, column):
        if self._board[line][column] != ' ':
            return False, 'You can\'t play there, position already occupied.'
        return True, None

    def _check_winning_condition(self, player):
        return any([
            all([self._board[i][j] == player for j in range(3)]) for i in range(3)
        ] + [
            all([self._board[j][i] == player for j in range(3)]) for i in range(3)
        ] + [
            all([self._board[i][i] == player for i in range(3)]),
            all([self._board[i][2-i] == player for i in range(3)]),
        ])
