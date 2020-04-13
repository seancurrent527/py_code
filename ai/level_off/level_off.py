import game, search, problems, reinforcement
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type = str, default='scenarios/scene1.txt', help='The scenario file to run.')
    parser.add_argument('-s', '--search', type = str, default='', help='The search algorithm to use.')
    parser.add_argument('-p', '--pause', type = float, default='0.0', help='The amount of time to pause in-between actions.')
    parser.add_argument('-t', '--trials', type = int, default=100, help='The number of trials to use during reinforcement learning.')
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
        elif args.search == 'qlearning':
            problem = problems.LevelProblem(gameState)
            qAgent = reinforcement.QAgent(alpha=0.4, gamma=0.6, epsilon=0.2)
            qAgent.fit(problem, args.trials)
            searchFunction = qAgent.search
        else:
            searchFunction = getattr(search, args.search)
        problem = problems.LevelProblem(gameState)
        solution = searchFunction(problem)
        playing = game.Game(gameState, game.Game.actionFromList(solution))
    playing.run(pause=args.pause)
    if args.search:
        print('Nodes expanded: ', problem.expanded)


if __name__ == '__main__':
    main()
    