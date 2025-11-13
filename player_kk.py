from pico2d import load_image, get_time, load_font, draw_rectangle, pico2d_image_loader
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT
import os


import game_framework

from state_machine import StateMachine

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0  # Km / Hour
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

class Run:
    def __init__(self, kk):
        self.player_kk = kk
        self.run_frame = 0

    def enter(self, e):
        self.run_frame = 0
        if right_down(e):
            self.player_kk.dir = 1
            self.player_kk.load_image(f'kk_backwalk_{self.run_frame}.png')
        elif left_down(e):
            self.player_kk.dir = -1
            self.player_kk.load_image(f'kk_walk_{self.run_frame}.png')

    def exit(self, e):
        pass

    def do(self):
        self.run_frame = (self.run_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        if self.player_kk.dir == -1:
            self.player_kk.load_image(f'kk_walk_{int(self.run_frame)}.png')
        elif self.player_kk.dir == 1:
            self.player_kk.load_image(f'kk_backwalk_{int(self.run_frame)}.png')

        self.player_kk.x += self.player_kk.dir * RUN_SPEED_PPS * game_framework.frame_time
        if self.player_kk.x < 50:
            self.player_kk.x = 50
        elif self.player_kk.x > 1230:
            self.player_kk.x = 1230

    def draw(self):
        if self.player_kk.face_dir == 1:
                self.player_kk.image.clip_composite_draw(0, 0, 62, 107, 0, 'h',
                                                     self.player_kk.x, self.player_kk.y,150,300)
        else:
            if self.player_kk.dir == 1:
                self.player_kk.image.clip_composite_draw(0, 0, 62, 107, 0, '0',
                                                     self.player_kk.x, self.player_kk.y,150,300)

class Idle:
    def __init__(self, kk):
        self.player_kk = kk
        self.idle_frame = 0

    def enter(self, e):
        self.player_kk.dir = 0
        self.player_kk.load_image(f'kk_walk_{int(self.idle_frame)}.png')
        self.idle_frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.idle_frame = (self.idle_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.player_kk.load_image(f'kk_idle_{int(self.idle_frame)}.png')

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
        self.load_image(f'kk_idle_{self.frame}.png')

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.state_machine = StateMachine(
            self.IDLE,
{
            self.IDLE: {right_down: self.RUN, left_down: self.RUN},
            self.RUN: {right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE,
               left_down: self.IDLE},
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