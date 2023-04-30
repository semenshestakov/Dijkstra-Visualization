import pygame as pg
from dijkstra import *
from paint import Paint, Colors
import sys
import time
import numpy as np
from graphs import Graph

class Interface:
    def __init__(self, size=400, size_rect=10):
        size = size // size_rect * size_rect
        self.size = size
        self.rect = size_rect

        self.sc = pg.display.set_mode((size, size))
        pg.display.set_caption("Dijkstra on Pygame - start")

        self.colors = Colors
        self.paint = Paint(self.sc, self.rect)

    def loop(self):
        x, y = 0, 0
        self.clear()
        clock = pg.time.Clock()

        fldraw = False

        fldel = False
        flstart = True
        flwall = False
        flend = False

        while True:
            for event in pg.event.get():

                match event.type:

                    case pg.QUIT:
                        sys.exit()

                    case pg.MOUSEMOTION:
                        x, y = event.pos

                    case pg.MOUSEBUTTONDOWN:
                        fldraw = True
                    case pg.MOUSEBUTTONUP:
                        fldraw = False

                    case pg.KEYDOWN if event.key == pg.K_CAPSLOCK:
                        self.generate_map()

                    case pg.KEYDOWN if event.key == pg.K_1:
                        flstart = self.start_check(flstart)
                        flwall = not flwall
                        flend = False
                        fldel = False

                    case pg.KEYDOWN if event.key == pg.K_2:
                        flend = not flend
                        fldel = False

                        if flend:
                            pg.display.set_caption("Dijkstra on Pygame - end")
                        else:
                            self.start_check(not flstart)

                    case pg.KEYDOWN if event.key == pg.K_3:
                        fldel = self.del_check(fldel, flstart, flend)

                    case pg.KEYDOWN if event.key == pg.K_BACKSPACE:
                        self.clear()

                    case pg.KEYDOWN if event.key == pg.K_TAB:
                        G, start, finish = self.sсan_window(sleep=0)


                        for point in start:
                            dijkstra = Dijkstra(G, point)
                            try:
                                dijkstra.start_algorithm()
                            except KeyError:
                                continue

                            for fin in finish:
                                stak = dijkstra.start_finish(fin)
                                if stak is None:
                                    continue
                                for p in stak:
                                    if p not in self.hash_map:
                                        self.paint(*p, self.colors.GREEN)

            x, y = x // self.rect * self.rect, y // self.rect * self.rect

            if fldel and fldraw:
                self.paint(x, y, self.colors.GRAY)
                if (x, y) in self.hash_map:
                    del self.hash_map[(x, y)]

            elif flend and fldraw:
                self.paint(x, y, self.colors.BLUE)
                self.hash_map[(x, y)] = "end"

            elif flstart and fldraw:
                self.paint(x, y, self.colors.YELLOW)
                self.hash_map[(x, y)] = "start"

            elif flwall and fldraw:
                self.paint(x, y, self.colors.RED)
                self.hash_map[(x, y)] = "wall"

            clock.tick(120)

    def sсan_window(self, sleep=0):
        starts = [
            k for k in self.hash_map
            if self.hash_map.get(k, None) == "start"
        ]
        finish = [
            k for k in self.hash_map
            if self.hash_map.get(k, None) == "end"
        ]
        FIFO = deque(starts)
        data = CreateData()
        temp = (
            (0, self.rect),
            (0, -self.rect),
            (self.rect, 0),
            (-self.rect, 0)
        )
        viz = set()

        while len(FIFO):
            point = FIFO.popleft()
            if point in viz:
                continue
            if point not in self.hash_map:
                self.paint(*point, self.colors.WHITE)

            for a, b in temp:

                p = (point[0] + a, point[1] + b)
                if any([
                    self.size <= p[0], 0 > p[0],
                    self.size <= p[1], 0 > p[1]
                ]):
                    continue

                if not (p in viz) and \
                        (self.hash_map.get(p, None) == None or "end") and \
                        self.hash_map.get(p, None) != "wall":
                    FIFO.append(p)
                    data(point, p)
                    time.sleep(sleep)

            viz.add(point)

        return data.G, starts, finish

    def start_check(self, fl):
        if fl:
            pg.display.set_caption("Dijkstra on Pygame - paint")
        else:
            pg.display.set_caption("Dijkstra on Pygame - start")
        fl = not fl
        return fl

    def del_check(self, fl, fls, fle):
        fl = not fl
        if fl:
            pg.display.set_caption("Dijkstra on Pygame - del")
        elif fle:
            pg.display.set_caption("Dijkstra on Pygame - end")
        else:
            self.start_check(not fls)

        return fl

    def clear(self):
        self.hash_map = {}

        for x in range(0, self.size, self.rect):
            for y in range(0, self.size, self.rect):
                self.paint(x, y, self.colors.GRAY, False)

        pg.display.update()

    def generate_map(self,v0=0.2,v1=0.7,v2=0.8):
        self.clear()
        size = self.size // self.rect

        gen_map = np.random.normal(size=(size, size))
        m1, m2 = np.max(gen_map), np.min(gen_map)

        for i in range(size):
            for j in range(size):
                x, y = i * self.rect, j * self.rect
                if gen_map[i][j] < m2 * v0:
                    self.paint(x, y, self.colors.RED)
                    self.hash_map[(x, y)] = "wall"
                elif gen_map[i][j] > v2*m1:
                    self.paint(x, y, self.colors.YELLOW)
                    self.hash_map[(x, y)] = "start"

                elif gen_map[i][j] > v1 * m1:
                    self.paint(x, y, self.colors.BLUE)
                    self.hash_map[(x, y)] = "end"
                else:
                    self.paint(x, y, self.colors.GRAY)


if __name__ == '__main__':
    interface = Interface(600, 20)
    interface.loop()
