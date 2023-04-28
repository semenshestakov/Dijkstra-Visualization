from collections import deque
from paint import Colors

class CreateData:
    def __init__(self):
        self.G = {}

    def __call__(self,p1,p2):
        if self.G.get(p1,False) is False:
            self.G[p1] = {}

        if self.G.get(p2,False) is False:
            self.G[p2] = {}

        self.G[p2][p1] = 1
        self.G[p1][p2] = 1





class Dijkstra:
    def __init__(self, G, start):
        self.G = G
        self.Gm = {k: None for k in G}
        self.Gm[start] = 0
        self.drque = deque([start])
        self.start = start

    def start_algorithm(self):
        while self.drque:
            point = self.drque.popleft()
            for key, value in self.G[point].items():
                if self.Gm[key] is None:
                    self.Gm[key] = value + self.Gm[point]
                    self.drque.append(key)
                elif self.Gm[key] + value < self.Gm[point]:
                    self.Gm[point] = self.Gm[key] + value
                    self.drque.append(point)
                elif self.Gm[key] > self.Gm[point] + value:
                    self.Gm[key] = self.Gm[point] + value
                    self.drque.append(key)

    def start_finish(self, finish, stak=...):
        stak = [] if stak is ... else stak[:]
        stak.append(finish)
        if self.start == finish:
            return stak
        for key, value in self.G[finish].items():
            if self.Gm[finish] - value == self.Gm[key]:
                return self.start_finish(key, stak)



