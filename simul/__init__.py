import os

import pygame as pg
import pymunk
from pymunk.pygame_util import DrawOptions
from pymunk.bb import Vec2d

from simul.settings import HEIGHT, WIDTH, FPS
from pymunk.constraints import *
from .AgentManager import AgentManager
from .models import Equilibrium,EquilibriumGA,Drone,DroneGA

#time
from datetime import datetime
from datetime import timedelta


class NoSuchModel(Exception):
    pass


class App:
    is_running = True
    objects = []
    __speed = 1
    k_left: bool = False
    k_right: bool = False
    frames_from_draw: int = 1
    models = {
        'eq_model': (Equilibrium, EquilibriumGA),
        'drone_model': (Drone, DroneGA)
    }

    def __init__(self,
                 w: int,
                 h: int,
                 fps: int):

        self.space = pymunk.Space()
        self.space.gravity = 0, 98.1
        self.graphics = os.environ['gs']
        if not self.graphics:
            print('Graphics disabled')
        model = self.models[os.environ.get('model_name')]
        if model is None:
            raise NoSuchModel(f"Model {os.environ.get('model_name')} is not exists")
        if self.graphics:
            pg.font.init()
            self.work_font: pg.font.Font = pg.font.SysFont('Comic Sans MS', 30)
            self.window = pg.display.set_mode(
                (WIDTH, HEIGHT)
            )
            self.options = DrawOptions(self.window)
        self.width = w
        self.height = h
        self.fps = fps
        self.clock = pg.time.Clock()
        self.__DELTA_TIME = 1.0/float(fps)
        self.agent_pos = Vec2d(self.width // 2, self.height - 120)
        self.manager = AgentManager(self, model)
        self.generation = 0
        #time
        self.genStartTime = 0
        self.maxDeltaTime = 0

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
        self.window.blit(generation,(15,5))
        speed = self.work_font.render(f"Speed: x{self.speed}",False,(255,255,255))
        self.window.blit(speed,(WIDTH/2-70,5))
        time_text = self.work_font.render(f"current:{self.genStartTime:.2f} max:{self.maxDeltaTime:.2f}", False, (255, 254, 254, .7))
        self.window.blit(time_text, (15, HEIGHT-50))

    #time
    def time_step(self):
        self.genStartTime += 1/FPS

    def update_time(self):
        self.maxDeltaTime = self.maxDeltaTime if self.maxDeltaTime>self.genStartTime else self.genStartTime
        self.genStartTime = 0

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
        if self.graphics:
            keys = pg.key.get_pressed()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                    del self.space
            if keys[pg.K_LEFT]:
                if not self.k_left:
                    self.speed -= 10 if keys[pg.K_LSHIFT] else 1
                    self.k_left = True
            else:
                self.k_left = False

            if keys[pg.K_RIGHT]:
                if not self.k_right:
                    self.speed += 10 if keys[pg.K_LSHIFT] else 1
                    self.k_right = True
            else:
                self.k_right = False
            self.time_step()
            self.draw()
        self.space.step(self.__DELTA_TIME)


    def test(self):
        self.drone_Agent = DroneAgent(self.space)
        while True:
            self.iter()

    def run(self):
        self.manager.start()
        #while self.is_running:
            # self.iter()


def start():
    app = App(WIDTH,HEIGHT,60)
    app.run()


def test():
    app = App(WIDTH,HEIGHT,60)
    app.test()
