import game, search, problems, reinforcement
import argparse, os

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type = str, default='scenarios/training/basic.txt', help='The scenario file to run.')
    parser.add_argument('-s', '--search', type = str, default='', help='The search algorithm to use.')
    parser.add_argument('-p', '--pause', type = float, default='0.0', help='The amount of time to pause in-between actions.')
    parser.add_argument('-t', '--trials', type = int, default=100, help='The number of trials to use during reinforcement learning.')
    parser.add_argument('-l', '--load', type = str, default = 'models/deepq.h5',
                        help='Model weights to load for deepq learing. If the path does not exist, a new model will be made.')
    parser.add_argument('-g', '--gpu', action = 'store_true', help="Whether or not to use GPU during Deep Q learning.")
    parser.add_argument('-d', '--directory', type = str, default = '',
                        help='The directory of files to train on. Only used with Deep Q learning.')
    return parser.parse_args()

def main():
    args = parse_args()
    if not args.gpu:
        os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
    gameState = game.GameState.fromFile(args.file)
    if not args.search:
        playing = game.Game(gameState, game.Game.actionFromPlayer())
    else:
        problem = problems.LevelProblem(gameState)
        if args.search == 'astar':
            searchFunction = search.aStar(search.distanceHeuristic)
        elif args.search == 'qlearning':
            qAgent = reinforcement.QAgent(alpha=0.9, gamma=0.6, epsilon=0.2)
            qAgent.fit(problem, args.trials)
            searchFunction = qAgent.search
        elif args.search == 'deepq':
            _, startState = problem.getStartState()
            model = reinforcement.getModel((len(startState), len(startState[0]), 4))
            if os.path.exists(args.load):
                model.load_weights(args.load)
            model.compile(loss = 'mse', optimizer = 'adam')
            deepQ = reinforcement.DeepQAgent(model, alpha=1.0, gamma=0.8, epsilon=0.3)
            if args.directory:
                trainingSet = problems.ProblemSet.fromDirectory(args.directory)
                deepQ.fitProblemSet(trainingSet, args.trials)
                deepQ.searchAll(trainingSet, record=True)
            else:
                deepQ.fit(problem, args.trials)
            deepQ.save(args.load)
            searchFunction = deepQ.search
        else:
            searchFunction = getattr(search, args.search)
        solution = searchFunction(problem)
        playing = game.Game(gameState, game.Game.actionFromList(solution))
    playing.run(pause=args.pause)
    if args.search:
        print('Nodes expanded: ', problem.expanded)


if __name__ == '__main__':
    main()
    