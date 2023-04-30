import pygame as pg
from dijkstra import *


class Colors:
    YELLOW = (244, 202, 22)
    RED = (255, 21, 61)
    BLACK = (0, 0, 0)
    BLUE = (0, 107, 200)
    WHITE = (255, 255, 255)
    GREEN = (124, 252, 0)
    GRAY = (105, 105, 105)


class Paint:

    def __init__(self, sc, rect):
        self.sc = sc
        self.rect = rect

    def __call__(self, x, y, col, update=True):
        rect = pg.draw.rect(
            self.sc,
            col,
            (x, y, self.rect - 1, self.rect - 1)
        )
        if update:
            pg.display.update(rect)

    def dijkstra_paint(self, G, start, finish, hash_map, gen=False):
        gen = Dijkstra.dijkstra_gen(G, start, finish)
        staks = [i[-1] for i in gen]
        for s in staks:
            for p in s:
                if p not in hash_map:
                    self(*p, Colors.GREEN, False)
