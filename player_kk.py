from pico2d import load_image, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_UP, SDLK_k, SDLK_j, SDLK_DOWN
import os


import game_framework

from state_machine import StateMachine

time_out = lambda e: e[0] == 'TIMEOUT'

def k_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_k

def k_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_k

def j_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_j

def j_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_j

def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP

def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN

def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN

jumpattack_k_frame = 0

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

class Skill2:
    def __init__(self, kk):
        self.player_kk = kk
        self.skill2_frame = 0

    def enter(self, e):
        self.player_kk.load_image('kk_skill2_sprite.png')
        self.skill2_frame = 0
        self.player_kk.y = 300

    def exit(self, e):
        self.player_kk.y = 200

    def do(self):
        self.skill2_frame = (self.skill2_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * 3) % 28
        if self.skill2_frame >= 27:
            self.player_kk.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.player_kk.face_dir == 1:
            self.player_kk.image.clip_composite_draw(217*int(self.skill2_frame), 0, 217, 220, 0, 'h',
                                                     self.player_kk.x, self.player_kk.y,520,520)
        else:
            self.player_kk.image.clip_composite_draw(217*int(self.skill2_frame), 0, 217, 220, 0, '0',
                                                     self.player_kk.x, self.player_kk.y,520,520)

class Skill1:
    def __init__(self, kk):
        self.player_kk = kk
        self.skill1_frame = 0

    def enter(self, e):
        self.player_kk.load_image('kk_skill1_sprite.png')
        self.skill1_frame = 0
        self.player_kk.y = 300

    def exit(self, e):
        self.player_kk.y = 200

    def do(self):
        self.skill1_frame = (self.skill1_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * 3) % 30
        if self.skill1_frame >= 29:
            self.player_kk.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.player_kk.face_dir == 1:
            self.player_kk.image.clip_composite_draw(155*int(self.skill1_frame), 0, 155, 245, 0, 'h',
                                                     self.player_kk.x, self.player_kk.y,400,600)
        else:
            self.player_kk.image.clip_composite_draw(155*int(self.skill1_frame), 0, 155, 245, 0, '0',
                                                     self.player_kk.x, self.player_kk.y,400,600)

class Jumpkick:
    def __init__(self, kk):
        self.player_kk = kk
        self.jumpkick_frame = 0

    def enter(self, e):
        global jumpattack_k_frame
        self.player_kk.load_image('kk_jumpattack_sprite.png')
        self.jumpkick_frame = jumpattack_k_frame

    def exit(self, e):
        self.player_kk.y = 200

    def do(self):
        self.jumpkick_frame = (self.jumpkick_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * 3) % 17
        if self.jumpkick_frame >= 16:
            self.player_kk.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.player_kk.face_dir == 1:
            self.player_kk.image.clip_composite_draw(113*int(self.jumpkick_frame), 0, 113, 193, 0, 'h',
                                                     self.player_kk.x, self.player_kk.y,300,500)
        else:
            self.player_kk.image.clip_composite_draw(113*int(self.jumpkick_frame), 0, 113, 193, 0, '0',
                                                     self.player_kk.x, self.player_kk.y,300,500)

class Punch:
    def __init__(self, kk):
        self.player_kk = kk
        self.punch_frame = 0

    def enter(self, e):
        self.punch_frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.punch_frame = (self.punch_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * 2) % 6
        if self.player_kk.face_dir == -1:
            self.player_kk.load_image(f'kk_punch_{int(self.punch_frame)}.png')
        elif self.player_kk.face_dir == 1:
            self.player_kk.load_image(f'kk_punch_{int(self.punch_frame)}.png')
        if self.punch_frame >= 5:
            self.player_kk.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.player_kk.face_dir == 1:
            self.player_kk.image.clip_composite_draw(0, 0, 131, 119, 0, 'h',
                                                     self.player_kk.x, self.player_kk.y,340,320)
        else:
            self.player_kk.image.clip_composite_draw(0, 0, 131, 119, 0, '0',
                                                     self.player_kk.x, self.player_kk.y,340,320)

class Kick:
    def __init__(self, kk):
        self.player_kk = kk
        self.kick_frame = 0

    def enter(self, e):
        self.kick_frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.kick_frame = (self.kick_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * 2) % 8
        self.player_kk.load_image(f'kk_kick_{int(self.kick_frame)}.png')
        if self.kick_frame >= 7:
            self.player_kk.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.player_kk.face_dir == 1:
            self.player_kk.image.clip_composite_draw(0, 0, 120, 111, 0, 'h',
                                                     self.player_kk.x, self.player_kk.y,300,300)
        else:
            self.player_kk.image.clip_composite_draw(0, 0, 120, 111, 0, '0',
                                                     self.player_kk.x, self.player_kk.y,300,300)

class Jump:
    def __init__(self, kk):
        self.player_kk = kk
        self.jump_frame = 0

    def enter(self, e):
        self.jump_frame = 0
        self.player_kk.y = 350


    def exit(self, e):
        global  jumpattack_k_frame
        self.player_kk.dir = 0
        jumpattack_k_frame = self.jump_frame

    def do(self):
        self.jump_frame = (self.jump_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * 3) % 14

        self.player_kk.load_image(f'kk_jump_sheet.png')

        self.player_kk.x += self.player_kk.dir * RUN_SPEED_PPS * game_framework.frame_time

        if self.player_kk.x < 50:
            self.player_kk.x = 50
        elif self.player_kk.x > 1230:
            self.player_kk.x = 1230

        if self.jump_frame >= 13:
            self.player_kk.y = 200
            self.player_kk.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.player_kk.face_dir == 1:
            self.player_kk.image.clip_composite_draw(67 * int(self.jump_frame), 0, 67, 201, 0, 'h',
                                                     self.player_kk.x, self.player_kk.y,180,600)
        else:
            self.player_kk.image.clip_composite_draw(67 * int(self.jump_frame), 0, 67, 201, 0, '0',
                                                     self.player_kk.x, self.player_kk.y,180,600)

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
        if self.player_kk.face_dir == 1:
            if self.player_kk.dir == -1:
                self.player_kk.load_image(f'kk_walk_{int(self.run_frame)}.png')
            elif self.player_kk.dir == 1:
                self.player_kk.load_image(f'kk_backwalk_{int(self.run_frame)}.png')
        else:
            if self.player_kk.dir == 1:
                self.player_kk.load_image(f'kk_walk_{int(self.run_frame)}.png')
            elif self.player_kk.dir == -1:
                self.player_kk.load_image(f'kk_backwalk_{int(self.run_frame)}.png')

        self.player_kk.x += self.player_kk.dir * RUN_SPEED_PPS * game_framework.frame_time
        if self.player_kk.x < 50:
            self.player_kk.x = 50
        elif self.player_kk.x > 1230:
            self.player_kk.x = 1230

    def draw(self):
        if self.player_kk.face_dir == 1:
            if self.player_kk.dir == -1:
                self.player_kk.image.clip_composite_draw(0, 0, 62, 107, 0, 'h',
                                                     self.player_kk.x, self.player_kk.y,150,300)
            else:
                self.player_kk.image.clip_composite_draw(0, 0, 62, 107, 0, 'h',
                                                     self.player_kk.x, self.player_kk.y,150,300)
        else:
            if self.player_kk.dir == 1:
                self.player_kk.image.clip_composite_draw(0, 0, 62, 107, 0, '0',
                                                     self.player_kk.x, self.player_kk.y,150,300)
            else:
                self.player_kk.image.clip_composite_draw(0, 0, 62, 107, 0, '',
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

        self.input_buffer = []

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.JUMP = Jump(self)
        self.KICK = Kick(self)
        self.PUNCH = Punch(self)
        self.JUMPKICK = Jumpkick(self)
        self.SKILL1 = Skill1(self)
        self.SKILL2 = Skill2(self)

        def skill1_command(e):
            if k_down(e) and self.input_buffer == ['DOWN', 'J', 'K']:
                self.input_buffer = []
                return True
            return False

        def skill2_command(e):
            if j_down(e) and self.input_buffer == ['DOWN', 'JUMP', 'J']:
                self.input_buffer = []
                return True
            return False


        self.state_machine = StateMachine(
            self.IDLE,
{
            self.IDLE: {right_down: self.RUN, left_down: self.RUN, up_down: self.JUMP,
                        (lambda e: k_down(e) and skill1_command(e)):self.SKILL1,
                        (lambda e: j_down(e) and skill2_command(e)):self.SKILL2,
                        k_down: self.KICK, j_down: self.PUNCH},
            self.RUN: {right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE,
               left_down: self.IDLE, up_down: self.JUMP, k_down: self.KICK, j_down: self.PUNCH},
            self.JUMP: {time_out: self.IDLE,
                        (lambda e, jj=self.JUMP: k_down(e) and jj.jump_frame < 7): self.JUMPKICK},
            self.JUMPKICK: {time_out: self.IDLE},
            self.KICK: {time_out: self.IDLE},
            self.PUNCH: {time_out: self.IDLE},
            self.SKILL1: {time_out: self.IDLE},
            self.SKILL2: {time_out: self.IDLE},
            }
        )

    def load_image(self, path):
        self.image = load_resource(path)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_DOWN:
                self.input_buffer = []
                name = 'DOWN'
            elif event.key == SDLK_j:
                name = 'J'
            elif event.key == SDLK_k:
                name = 'K'
            elif event.key == SDLK_UP:
                name = 'JUMP'
            else:
                name = None

            if name :
                self.input_buffer.append(name)
                if len(self.input_buffer) > 3 and self.input_buffer[2]=='K':
                    self.input_buffer.clear()
                    self.state_machine.handle_state_event(('SKILL1_INPUT',event))
                    return
                elif len(self.input_buffer) > 3 and self.input_buffer[2] == 'J':
                    self.input_buffer.clear()
                    self.state_machine.handle_state_event(('SKILL2_INPUT', event))
                    return
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 40, self.y - 130, self.x + 55, self.y + 130

    def handle_collision(self, group, other):
        pass