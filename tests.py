import unittest
import graphs
import numpy as np


class TestGraphFunc(unittest.TestCase):
    def setUp(self):
        self.graph = graphs.Graph({})

    def test_1merge_graph_points(self):
        test_graph = np.zeros((1, 9, 9), dtype=float)
        test_point = np.zeros((1, 3, 3), dtype=float)

        test_point[0, 0, 0] = 1
        test_point[0, 1, 1] = 1

        res = np.zeros((1, 9, 9), dtype=float)
        res[0, 0, 0] = 2
        res[0, 4, 4] = 2


        result = self.graph.merge_graph_points(test_graph, test_point)
        self.assertEqual(True,(result == res).all())

    def test_2merge_graph_points(self):
        test_graph = np.zeros((1, 9, 9), dtype=float)
        test_point = np.zeros((1, 3, 3), dtype=float)

        test_point[0, 1, 2] = 1
        res = np.zeros((1, 9, 9), dtype=float)
        res[0,5,5] = 2

        result = self.graph.merge_graph_points(test_graph, test_point)
        self.assertEqual(True, (result == res).all())

    def test_3merge_graph_points(self):
        test_graph = np.zeros((1, 9, 9), dtype=float)
        test_point = np.zeros((1, 3, 3), dtype=float)

        res = np.zeros((1, 9, 9), dtype=float)
        result = self.graph.merge_graph_points(test_graph, test_point)

        self.assertEqual(True, (result == res).all())

if __name__ == '__main__':
    unittest.main()