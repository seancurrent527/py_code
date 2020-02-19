import game
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type = str, default='scenarios/scene1.txt', help='The scenario file to run.')
    return parser.parse_args()

def readScene(file):
    with open(file) as fp:
        return fp.read()

def __main__():
    args = parse_args()
    format_string = readScene(args.file)
    gameState = game.GameState(format_string)
    playing = game.Game(gameState, game.Game.actionFromPlayer)
    playing.run()

if __name__ == '__main__':
    main()
    