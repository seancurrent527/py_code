from queue import Queue
from stack import Stack

class NeighborNode:
    def __init__(self, nvn):
        self.vertex_number = nvn
        self.next = None
        
class Vertex:
    def __init__(self):
        self.next = None
        
    def insert_neighbor(self, nvn):
        temp = NeighborNode(nvn)
        temp.next = self.next
        self.next = temp
    
        self.next, self.next.next = NeighborNode(nvn), self.next
        
    def get_neighbors(self):
        neighbors = []
        v = self # Vertex object
        while v.next:
            v = v.next # NeighborNode object as soon as this happens
            neighbors.append(v.vertex_number)
        return neighbors
        
class GraphAL:
    def __init__(self, name='', fname=None):
        self.name = name
        self.adjacency_list = []
        if fname:
            with open(fname) as fp:
                for i, line in enumerate(fp):
                    self.adjacency_list.append(Vertex())
                    neighbors = line.split()
                    for n in neighbors:
                        self.adjacency_list[i].insert_neighbor(int(n))
    
    def shortest_path(self, start, end):
        self.adjacency_list[start].parent = None
        S = Queue()
        D = {start}
        S.enqueue(start)
        while not S.is_empty():
            v = S.dequeue()
            D.add(v)
            if v == end:
                ls = [v]
                while self.adjacency_list[v].parent is not None:
                    v = self.adjacency_list[v].parent
                    ls.append(v)
                return ls
            for w in self.adjacency_list[v].get_neighbors():
                if w not in D:
                    D.add(w)
                    self.adjacency_list[w].parent = v
                    S.enqueue(w)
    
def main():
    g = GraphAL(fname = 'graph_connected.txt')
    print(g.shortest_path(0, 0))
    print(g.shortest_path(0, 1))
    print(g.shortest_path(0, 2))
    print(g.shortest_path(0, 4))
    print(g.shortest_path(4, 7))
    print(g.shortest_path(8, 5))
    print(g.shortest_path(1, 9))
    print(g.shortest_path(9, 1))
    
if __name__ == '__main__':
    main()    