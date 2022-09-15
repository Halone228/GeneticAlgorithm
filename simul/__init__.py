import pygame as pg
import pymunk
from pymunk.pygame_util import DrawOptions

class App:
    is_running = True
    def __init__(self,
                 w: int,
                 h: int,
                 fps: int):
        self.window = pg.display.set_mode(
            (w,h)
        )
        self.space = pymunk.Space()
        self.options = DrawOptions(self.window)
        self.fps = fps
        self.clock = pg.time.Clock()
        self.__DELTA_TIME = self.clock.tick(self.fps)

    def draw(self):
        self.window.fill((0, 0, 0))
        self.space.debug_draw(self.options)

    def iter(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False

    ###############

    def run(self):
        while self.is_running:
            self.iter()
            self.draw()
            self.clock.tick(self.fps)

if __name__=='__main__':
    app = App(720,720,60)
    app.run()
