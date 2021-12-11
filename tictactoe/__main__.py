import signal
import sys

from tictactoe.game import Game
from tictactoe.player import Player
from tictactoe.rl_player import RLPlayer


def main():
    player1 = RLPlayer('O', 0.9)
    player1.load_values('bot_values')
    player2 = Player('X')
    game = Game(player2, player1)

    def sigint_handler(sig, frame):
        player1.save_values('bot_values')
        sys.exit(0)
    signal.signal(signal.SIGINT, sigint_handler)

    while(True):
        game.reset()
        game.render()
        while not game.ended():
            game.get_input()
            game.process()
            game.render()
            # player2.print_values()
        game.render()
        input('Press ENTER to play again')


if __name__ == '__main__':
    main()
