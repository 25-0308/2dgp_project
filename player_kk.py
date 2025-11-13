from pico2d import load_image, get_time, load_font, draw_rectangle, pico2d_image_loader
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT
import os

import game_world
import game_framework

from state_machine import StateMachine


def space_down(e): # e is space down ?
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

time_out = lambda e: e[0] == 'TIMEOUT'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4


def load_resource(path):
    base_dir = os.path.dirname(__file__)
    abs_path = os.path.join(base_dir, 'kk', path)
    return load_image(abs_path)

class Idle:
    def __init__(self, kk):
        self.player_kk = kk

    def enter(self, e):
        self.player_kk.wait_time = get_time()
        self.player_kk.dir = 0

    def exit(self, e):
        pass

    def do(self):
        self.player_kk.frame = (self.player_kk.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        self.player_kk.load_image(f'kk_{int(self.player_kk.frame)}.png',)

    def draw(self):
        if self.player_kk.face_dir == 1:
            self.player_kk.image.clip_composite_draw(0, 0, 128, 244, 0, '',
                                                     self.player_kk.x, self.player_kk.y,150,300)
        else:
            self.player_kk.image.clip_composite_draw(0, 0, 128, 244, 0, 'h',
                                                     self.player_kk.x, self.player_kk.y,150,300)

class Playerkk:
    def __init__(self):
        self.x, self.y = 950, 200
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.load_image(f'kk_{self.frame}.png')

        self.IDLE = Idle(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {space_down: self.IDLE},
            }
        )

    def load_image(self, path):
        self.image = load_resource(path)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 40, self.y - 130, self.x + 55, self.y + 130

    def handle_collision(self, group, other):
        pass