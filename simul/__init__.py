import pygame as pg
import pymunk
from pymunk.pygame_util import DrawOptions
from pymunk.bb import Vec2d

from simul.settings import HEIGHT, WIDTH
from .objects import *
from pymunk.constraints import *
from .AgentManager import AgentManager
from .models import Equilibrium,EquilibriumGA


class App:
    is_running = True
    objects = []
    __speed = 1
    k_left: bool = False
    k_right: bool = False
    frames_from_draw: int = 1

    def __init__(self,
                 w: int,
                 h: int,
                 fps: int):
        pg.font.init()
        self.work_font: pg.font.Font = pg.font.SysFont('Comic Sans MS', 30)
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
        self.manager = AgentManager(self, (Equilibrium, EquilibriumGA))
        self.generation = 0

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, value):
        if value < 1:
            self.__speed = 1
        else:
            self.__speed = value

    def build_texts(self):
        generation = self.work_font.render(f"Generation: {self.generation}",False,(255,255,255))
        self.window.blit(generation,(50,50))
        speed = self.work_font.render(f"Speed: x{self.speed}",False,(255,255,255))
        self.window.blit(speed,(500,50))

    def draw(self):
        if self.frames_from_draw % self.speed == 0:
            self.window.fill((0, 0, 0))
            self.space.debug_draw(self.options)
            self.build_texts()
            pg.display.flip()
            self.frames_from_draw = 1
            self.clock.tick(self.fps)
        else:
            self.frames_from_draw += 1

    def iter(self):
        self.space.step(self.__DELTA_TIME)
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
        if keys[pg.K_LEFT]:
            if not self.k_left:
                self.speed -= 1
                self.k_left = True
        else:
            self.k_left = False

        if keys[pg.K_RIGHT]:
            if not self.k_right:
                self.speed += 1
                self.k_right = True
        else:
            self.k_right = False

        self.draw()



    ###############

    def run(self):
        self.manager.start()
        #while self.is_running:
            # self.iter()



def start():
    app = App(WIDTH,HEIGHT,60)
    app.run()


if __name__=='__main__':
    app = App(720,720,60)
    app.run()
