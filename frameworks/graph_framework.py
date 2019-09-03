'''
graph_framework.py
'''

class Node:
    def __init__(self, value):
        self.value = value
        self.connections = {}

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value

    def add_connection(self, node):
        if node not in self.connections.values() and node != self:
            self.connections[node.value] = node

    def get_connection(self, value):
        if value not in self.connections:
            return None
        return self.connections[value]

    def remove_connection(self, value):
        self.connections.pop(value)

    def is_connected(self, other):
        return other in self.connections

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other.value

class Graph:
    def __init__(self):
        self.nodes = {}
        self.size = 0

    def __repr__(self):
        retval = 'Graph\n------------\n'
        for n in self.nodes.values():
            for n2 in n.connections:
                retval += n.value + ' --> ' + n2.value + '\n'
            retval += '------------\n'
        return retval

    def add_nodes(self, *nodes):
        for n in nodes:
            self.nodes[n.value] = n
            self.size += 1

    def add_connections(self, val1, vals, directed = False):
        for val2 in vals:
            self.nodes[val1].add_connection(self.nodes[val2])
            if not directed:
                self.nodes[val2].add_connection(self.nodes[val1])

    def remove_connection(self, val1, val2, both = True):
        self.nodes[val1].remove_connection(val2)
        if both:
            self.nodes[val2].remove_connection(val1)

    def __getitem__(self, val):
        return self.nodes[val]

    def __contains__(self, val):
        return val in self.nodes

class Path:
    def __init__(self, graph, curr = None, target = None, past = set()):
        self._graph = graph    
        self._curr = curr
        self._past = past
        self._target = target
        self.routes = self.search()

    def __repr__(self):
        stack_id = lambda item, *x: item[x[0]] if len(x) == 1 else stack_id(item[x[0]], x[1:])

    def search(self):
        routes = []
        if self._curr == self._target:
            return self._curr
        else:
            self._past.add(self._curr)
            for node in self._curr.connections.values():
                if node not in self._past:
                    plan = Path(self._graph, node, self._target, self._past).search()
                    if plan:
                        routes.append(plan)
            self._past.remove(self._curr)
            if routes:
                return [self._curr, routes]
            else:
                return routes
#=======================================================================
def main():
    net = Graph()
    nodes = [Node('A'), Node('B'), Node('C'), Node('D')]
    net.add_nodes(*nodes)
    for n in net.nodes:
        net.add_connections(n, net.nodes)
    net.remove_connection('B', 'D')
    
    router = Path(net, net['A'], net['D'])
    print(router.routes)

if __name__ == '__main__':
    main()
            
            

    

































