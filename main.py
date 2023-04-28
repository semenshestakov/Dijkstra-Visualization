import pygame as pg
from dijkstra import *
from paint import Paint, Colors
import sys
import time
from pprint import pprint


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
                        G, start, finish = self.sсan_window(sleep=0.001)

                        for point in start:
                            pprint(G)
                            dijkstra = Dijkstra(G, point)
                            dijkstra.start_algorithm()
                            for fin in finish:
                                stak = dijkstra.start_finish(fin)
                                print(stak)

                                for p in stak:
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

        while len(FIFO):
            point = FIFO.popleft()

            if point not in self.hash_map:
                self.paint(*point, self.colors.WHITE)

            # if self.hash_map[point] == self.colors.BLUE or self.colors.RED:

            for a, b in temp:

                p = (point[0] + a, point[1] + b)
                if any([
                    self.size < p[0], 0 > p[0],
                    self.size < p[1], 0 > p[1]
                ]):
                    continue

                if not (p in data.G) and self.hash_map.get(p, None) is None:
                    FIFO.append(p)
                    data(point, p)
                    time.sleep(sleep)

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


if __name__ == '__main__':
    interface = Interface(400, 20)
    interface.loop()
