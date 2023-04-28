import pygame as pg
from dijkstra import *
from paint import Paint, Colors
import sys


class PointRect:
    def __init__(self, x, y, col):


class Interface:
    def __init__(self, size=400, size_rect=10):
        size = size // size_rect * size_rect
        self.size = size
        self.rect = size_rect

        self.sc = pg.display.set_mode((size, size))
        pg.display.set_caption("Dijkstra on Pygame - start")

        self.colors = Colors
        self.paint = Paint(self.sc, self.rect)
        self.alg = Dijkstra()

    def loop(self):
        x, y = 0, 0
        self.clear()

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

                    case pg.KEYDOWN if event.key == pg.K_DELETE or pg.K_BACKSPACE:
                        self.clear()

            x, y = x // self.rect * self.rect, y // self.rect * self.rect

            if fldel and fldraw:
                self.paint(x, y, self.colors.GRAY)
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

    def skan_window(self,start):
        starts = [k for k in self.hash_map if k == self.colors.YELLOW]
        FIFO = deque(starts)
        data = CreateData()
        while FIFO:
            point = FIFO.popleft()
            data(point)


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
