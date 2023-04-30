import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


class Graph:

    def __init__(self, graph, start, finish, step=20, n=30):
        self.graph = graph
        self.graph_to_map(step, n)

        self.start_finish_to_map(start, finish, step, n)

        # self.start = start
        # self.finish = finish

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
        self.start_finish_map = np.zeros((len(start), len(finish), n, n), dtype=np.int8)

        for i in range(len(start)):

            x, y = start[i]
            x, y = x // step, y // step
            self.start_finish_map[i, :, y, x] = 1
            for j in range(len(finish)):
                x1, y1 = finish[j]
                x1, y1 = x1 // step, y1 // step
                self.start_finish_map[:, j, y1, x1] = 1

        # self.start_finish_map.reshape(len(start) + len(finish), n, n)

    def graph_map_visualization(self):
        plt.imshow(self.graph_map)
        plt.show()

    def start_finish_map_visualization(self):
        res = np.sum(self.start_finish_map, axis=(0,1))
        print(res.shape)
        plt.imshow(res)
        plt.show()
