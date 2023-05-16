import pygame as pg
from dijkstra import *


class Colors:
    STARTP = (218,112,214)     # (244, 202, 22)
    WALLS = (255,69,0)       # (255, 21, 61)
    BLACK = (0, 0, 0)
    FINISHP = (0,191,255)     # (0, 107, 200)
    WHITE = (255, 255, 255)
    WAY = (124, 252, 0)         # (124, 252, 0)
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
                    self(*p, Colors.WAY, False)
