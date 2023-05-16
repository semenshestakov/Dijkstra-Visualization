import unittest
import graphs
import numpy as np


class TestGraphFunc(unittest.TestCase):
    def setUp(self):
        self.graph = graphs.Graph({})
        pass

    def test_merge_graph_points(self):
        test_graph = np.zeros((1, 9, 9), dtype=float)
        test_point = np.zeros((1, 3, 3), dtype=float)

        test_point[0, 0, 0] = 1
        test_point[0, 1, 1] = 1

        res = np.zeros((1, 9, 9), dtype=float)
        res[0, 0, 0] = 2
        res[0, 4, 4] = 2


        result = self.graph.merge_graph_points(test_graph, test_point)
        print(result == res)
        self.assertEqual(result,(result == res).all())


if __name__ == '__main__':
    unittest.main