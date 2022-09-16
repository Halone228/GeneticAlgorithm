import pygame as pg
import pymunk
from pymunk.pygame_util import DrawOptions
from pymunk.bb import Vec2d
from objects import *
from pymunk.constraints import *



class App:
    is_running = True
    objects = []
    def __init__(self,
                 w: int,
                 h: int,
                 fps: int):
        self.window = pg.display.set_mode(
            (w,h)
        )
        self.width = w
        self.height = h
        self.space = pymunk.Space()
        self.space.gravity = 0, 98.1
        self.options = DrawOptions(self.window)
        self.fps = fps
        self.clock = pg.time.Clock()
        self.__DELTA_TIME = 1.0/float(fps)
        self.__init_objects__()

    def __init_objects__(self):
        ground = Rect(Vec2d(.0,float(self.height)),self.width,100,is_dynamic=False,friction=0.1)
        ground.add_to_space(self.space)
        circle = Circle(Vec2d(300.0,.0),radius=20,friction=0.3)
        circle.add_to_space(self.space)
        self.objects.append(ground)
        self.objects.append(circle)
        Agent(self.space)

    def draw(self):
        self.window.fill((0, 0, 0))
        self.space.debug_draw(self.options)
        pg.display.flip()

    def iter(self):
        self.space.step(self.__DELTA_TIME)
        keys = pg.key.get_pressed()
        if keys[pg.K_h]:
            create_car(self.space,300, 200, 5)
        for object in self.objects:
            object.update()
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
