import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


class Graph:

    def __init__(self,graph,step=20,n=30):
        self.graph = graph
        self.graph_arr = np.zeros((n,n),dtype=np.int8)
        self.graph_to_map(step)


    def graph_to_map(self,step=20):
        """
        graph struct:
            dict{
                (int,int):dict{
                            (int,int):1, ...
                            }, ..
                }
        """
        for key_node in self.graph:
            x,y = key_node
            self.graph_arr[x][y] = 1
            for sub_node in self.graph[key_node]:
                x1,y1 = sub_node
                self.graph_arr[x1][y1] = 1

    def graph_map_visualization(self):
        plt.imshow(self.graph_arr)
        plt.show()









