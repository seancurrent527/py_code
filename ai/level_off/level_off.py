import game, search, problems
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type = str, default='scenarios/scene1.txt', help='The scenario file to run.')
    parser.add_argument('-s', '--search', type = str, default='', help='The search algorithm to use.')
    parser.add_argument('-p', '--pause', type = float, default='0.0', help='The amount of time to pause in-between actions.')
    return parser.parse_args()

def readScene(file):
    with open(file) as fp:
        return fp.read()

def main():
    args = parse_args()
    formatString = readScene(args.file)
    gameState = game.GameState(formatString)
    if not args.search:
        playing = game.Game(gameState, game.Game.actionFromPlayer())
    else:
        if args.search == 'astar':
            searchFunction = search.aStar(search.distanceHeuristic)
        else:
            searchFunction = getattr(search, args.search)
        problem = problems.LevelProblem(gameState)
        solution = searchFunction(problem)
        playing = game.Game(gameState, game.Game.actionFromList(solution))
        print('Cost: ', len(solution))
    playing.run(pause=args.pause)


if __name__ == '__main__':
    main()
    