class Player:
    def __init__(self, symbol):
        self._symbol = symbol

    @property
    def symbol(self):
        return self._symbol

    def get_input(self, board):
        position = input('Enter the position to play(1-9): ')
        while position > '9' or position < '1':
            position = input('Please enter a number between 1 and 9: ')
        index = int(position) - 1
        line = index//3
        column = index % 3
        return line, column

    def process(self, board, current_player):
        pass
