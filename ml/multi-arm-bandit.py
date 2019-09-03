'''
multi-arm-bandit.py
'''
import random, numpy as np, functools
import matplotlib.pyplot as plt

@functools.total_ordering
class Machine:
    def __init__(self, mu = 0, sigma = 1):
        self.mean = mu
        self.std = sigma
        self.gen = random.gauss
        self.gen_args = (mu, sigma)

    def __repr__(self):
        return 'Machine(' + str(self.mean) + ', ' + str(self.std) + ')'

    def __call__(self):
        return self.gen(*self.gen_args)

    def __eq__(self, other):
        return self.mean == other.mean

    def __lt__(self, other):
        return self.mean < other.mean

    def __hash__(self):
        return hash(self.gen_args)

class BanditHistory:
    def __init__(self, machines):
        self.machines = machines
        self.reward = []
        self.cum_reward = []
        self.regret = []
        self.machine_stats = [0 for i in range(len(machines))]
        self.machine_ns = [0 for i in range(len(machines))]
        self._curr_reward = 0

    def _regret(self):
        return len(self.reward) * max(self.machines).mean - self._curr_reward

    def add(self, machine, reward):
        self.machine_ns[machine] += 1 
        self.machine_stats[machine] += reward / self.machine_ns[machine]  
        self.reward.append(reward)
        self._curr_reward += reward
        self.cum_reward.append(self._curr_reward)
        self.regret.append(self._regret())

class Bandit:
    def __init__(self, machines):
        self.machines = machines
        self.num_machines = len(machines)
        self.reward = 0
        self.t = 0
        self.history = BanditHistory(machines)

    def generate(self, n = 1):
        for _ in range(n):
            self.t += 1
            i = random.randrange(0, self.num_machines)
            res = self.machines[i]()
            yield i, res
        
    def run(self, n = 1):
        for i, res in self.generate(n):
            self.history.add(i, res)
        
class EpsilonGreedy(Bandit):
    def __init__(self, machines, epsilon):
        Bandit.__init__(self, machines)
        self.epsilon = epsilon
        
    def generate(self, n = 1):
        for _ in range(n):
            self.t += 1
            if random.random() < self.epsilon:
                i = random.randrange(0, self.num_machines)
            else:
                i = max(range(self.num_machines), key = lambda x: self.history.machine_stats[x])
            res = self.machines[i]()
            yield i, res
   
class UCB1(Bandit):
    def generate(self, n = 1, initial = 0):
        for _ in range(initial):
            i = random.randrange(0, self.num_machines)
            res = self.machines[i]()
            yield i, res
        for _ in range(n - initial):
            if 0 in self.history.machine_ns:
                i = random.randrange(0, self.num_machines)
            else:
                opt = lambda i: self.history.machine_stats[i] + (2 * np.log(self.t) / self.history.machine_ns[i]) ** 0.5
                i = max(range(self.num_machines), key = opt)
            res = self.machines[i]()
            yield i, res

    def run(self, n = 1, initial = 0):
        for i, res in self.generate(n, initial):
            self.history.add(i, res)

#=====================================================================
def test():
    dist = {Machine(1, 1): 4,
            Machine(2, 0.1): 2,
            Machine(5, 2): 1}
    machines = [k  for k, v in dist.items() for _ in range(v)]
    mab = UCB1(machines)
    mab.run(1000, initial=200)
    plt.plot(np.arange(1000), mab.history.regret)
    plt.show()

if __name__ == '__main__':
    test()