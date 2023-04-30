import numpy as np
import matplotlib.pyplot as plt
from dijkstra import Dijkstra


class Graph:

    def __init__(self, graph, start, finish, stak, step=20, n=30):
        self.graph = graph
        self.start = start
        self.finish = finish

        self.graph_to_map(step, n)
        self.start_finish_map = self.start_finish_to_map(start, finish, step, n)
        self.result_map = self.stak_map(stak, step, n)

        self.step = step
        self.n = n

        # self.start = start
        # self.finish = finish

    def gen_data(self, start, finish, n):
        n1, n2 = len(start), len(finish)

        start_finish = np.zeros((n1 * n2, n, n))
        stak_map = np.zeros((n1 * n2, n, n))
        i = 0
        for point, fin, stak in Dijkstra.dijkstra_gen(self.graph, start, finish):
            map_points = self.start_finish_to_map([point], [fin], self.step, self.n)
            stak = self.stak_map([stak], self.step, self.n)
            start_finish[i] = np.squeeze(map_points)
            stak_map[i] = np.squeeze(stak)
            i += 1

        return start_finish, stak_map

    def graph_to_map(self, step, n):
        self.graph_map = np.zeros((n, n), dtype=np.int8)
        """
        graph struct:
            dict{
                (int,int):dict{
                            (int,int):1, ...
                            }, ..
                }
        """
        for key_node in self.graph:
            x, y = key_node
            y, x = x // step, y // step
            self.graph_map[x][y] = 1
            for sub_node in self.graph[key_node]:
                x1, y1 = sub_node
                y1, x1 = x1 // step, y1 // step
                self.graph_map[x1][y1] = 1

    def start_finish_to_map(self, start, finish, step, n):
        start_finish_map = np.zeros((len(start), len(finish), n, n), dtype=np.int8)

        for i in range(len(start)):

            x, y = start[i]
            x, y = x // step, y // step
            start_finish_map[i, :, y, x] = 1
            for j in range(len(finish)):
                x1, y1 = finish[j]
                x1, y1 = x1 // step, y1 // step
                start_finish_map[:, j, y1, x1] = 1

        return start_finish_map

        # self.start_finish_map.reshape(len(start) + len(finish), n, n)

    def graph_map_visualization(self):
        plt.imshow(self.graph_map)
        plt.show()

    def start_finish_map_visualization(self):
        res = np.sum(self.start_finish_map, axis=(0, 1))
        plt.imshow(res)
        plt.show()

    def stak_map_visualization(self):
        res = np.sum(self.result_map, axis=0)
        plt.imshow(res)
        plt.show()

    def stak_map(self, stak, step, n):
        result_map = np.zeros((len(stak), n, n))

        for i in range(len(stak)):
            for elem in stak[i]:
                x, y = elem
                x, y = x // step, y // step
                result_map[i, y, x] = 1

        return result_map

    def return_data(self):
        sf, res = self.gen_data(self.start, self.finish, self.n)
        return self.graph_map, sf, res
