import pygame as pg
import pymunk
from pymunk.pygame_util import DrawOptions
from pymunk.bb import Vec2d

from simul.settings import HEIGHT, WIDTH
from .objects import *
from pymunk.constraints import *
from .AgentManager import AgentManager



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
        self.agent_pos = Vec2d(self.width // 2, self.height - 120)
        self.__init_objects__()
        self.manager = AgentManager(self)

    def __init_objects__(self):
        ground = Rect(Vec2d(.0,float(self.height)),self.width,100,is_dynamic=False,friction=0.1)
        ground.add_to_space(self.space)
        self.objects.append(ground)
        # agent = Agent(self.space,self.agent_pos)
        # self.objects.append(agent)

    def draw(self):
        self.window.fill((0, 0, 0))
        self.space.debug_draw(self.options)
        pg.display.flip()

    def iter(self):
        self.space.step(self.__DELTA_TIME)
        keys = pg.key.get_pressed()
        for object in self.objects:
            object.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
        self.draw()
        self.clock.tick(self.fps*2)


    ###############

    def run(self):
        self.manager.ga.start()
        #while self.is_running:
            # self.iter()



def start():
    app = App(WIDTH,HEIGHT,60)
    app.run()


if __name__=='__main__':
    app = App(720,720,60)
    app.run()
