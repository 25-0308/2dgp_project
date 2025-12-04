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
    abs_path = os.path.join(base_dir, 'kyo', path)
    return load_image(abs_path)

class Skill2:
    def __init__(self, kyo):
        self.player_kyo = kyo
        self.skill2_frame = 0

    def enter(self, e):
        self.player_kyo.load_image('kyo_skill2_sprite.png')
        self.skill2_frame = 0
        self.player_kyo.y = 350

    def exit(self, e):
        self.player_kyo.y = 200

    def do(self):
        self.skill2_frame = (self.skill2_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * 2.5) % 19
        if self.skill2_frame >= 18:
            self.player_kyo.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.player_kyo.face_dir == 1:
            self.player_kyo.image.clip_composite_draw(121*int(self.skill2_frame), 0, 121, 196, 0, 'h',
                                                     self.player_kyo.x, self.player_kyo.y,300,575)
        else:
            self.player_kyo.image.clip_composite_draw(121*int(self.skill2_frame), 0, 121, 196, 0, '0',
                                                     self.player_kyo.x, self.player_kyo.y,300,575)

class Skill1:
    def __init__(self, kyo):
        self.player_kyo = kyo
        self.skill1_frame = 0

    def enter(self, e):
        self.player_kyo.load_image('kyo_skill1_0.png')
        self.skill1_frame = 0
        self.player_kyo.y = 250

    def exit(self, e):
        self.player_kyo.y = 200

    def do(self):
        self.skill1_frame = (self.skill1_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * 3) % 25
        self.player_kyo.load_image(f'kyo_skill1_{int(self.skill1_frame)}.png')
        if self.skill1_frame >= 24:
            self.player_kyo.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.player_kyo.face_dir == 1:
            self.player_kyo.image.clip_composite_draw(0, 0, 215, 122, 0, 'h',
                                                     self.player_kyo.x, self.player_kyo.y,400,400)
        else:
            self.player_kyo.image.clip_composite_draw(0, 0, 215, 122, 0, '0',
                                                     self.player_kyo.x, self.player_kyo.y,600,400)

class Jumpkick:
    def __init__(self, kyo):
        self.player_kyo = kyo
        self.jumpkick_frame = 0

    def enter(self, e):
        global jumpattack_k_frame
        self.player_kyo.load_image('kyo_jumpattack_sprite.png')
        self.jumpkick_frame = jumpattack_k_frame

    def exit(self, e):
        self.player_kyo.y = 200

    def do(self):
        self.jumpkick_frame = (self.jumpkick_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * 2.5) % 15
        if self.jumpkick_frame >= 14:
            self.player_kyo.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.player_kyo.face_dir == 1:
            self.player_kyo.image.clip_composite_draw(114*int(self.jumpkick_frame), 0, 114, 185, 0, 'h',
                                                     self.player_kyo.x, self.player_kyo.y,300,500)
        else:
            self.player_kyo.image.clip_composite_draw(114*int(self.jumpkick_frame), 0, 114, 185, 0, '0',
                                                     self.player_kyo.x, self.player_kyo.y,300,500)

class Punch:
    def __init__(self, kyo):
        self.player_kyo = kyo
        self.punch_frame = 0

    def enter(self, e):
        self.punch_frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.punch_frame = (self.punch_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * 1.5) % 7
        self.player_kyo.load_image(f'kyo_punch_sprite.png')
        if self.punch_frame >= 6:
            self.player_kyo.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.player_kyo.face_dir == 1:
            self.player_kyo.image.clip_composite_draw(112 * int(self.punch_frame), 0, 112, 106, 0, 'h',
                                                     self.player_kyo.x, self.player_kyo.y,300,300)
        else:
            self.player_kyo.image.clip_composite_draw(112 * int(self.punch_frame), 0, 112, 106, 0, '0',
                                                     self.player_kyo.x, self.player_kyo.y,300,300)

class Kick:
    def __init__(self, kyo):
        self.player_kyo = kyo
        self.kick_frame = 0

    def enter(self, e):
        self.kick_frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.kick_frame = (self.kick_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * 1.5) % 6
        self.player_kyo.load_image(f'kyo_kick_sprite.png')

        if self.kick_frame >= 5:
            self.player_kyo.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.player_kyo.face_dir == 1:
            self.player_kyo.image.clip_composite_draw(134*int(self.kick_frame), 0, 134, 113, 0, 'h',
                                                     self.player_kyo.x, self.player_kyo.y,350,320)
        else:
            self.player_kyo.image.clip_composite_draw(134*int(self.kick_frame), 0, 134, 113, 0, '0',
                                                     self.player_kyo.x, self.player_kyo.y,350,320)

class Jump:
    def __init__(self, kyo):
        self.player_kyo = kyo
        self.jump_frame = 0

    def enter(self, e):
        self.jump_frame = 0
        self.player_kyo.y = 350

    def exit(self, e):
        global jumpattack_k_frame
        self.player_kyo.dir = 0
        jumpattack_k_frame = self.jump_frame

    def do(self):
        self.jump_frame = (self.jump_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * 2.5) % 13

        self.player_kyo.load_image(f'kyo_jump_sprite.png')

        self.player_kyo.x += self.player_kyo.dir * RUN_SPEED_PPS * game_framework.frame_time

        if self.player_kyo.x < 50:
            self.player_kyo.x = 50
        elif self.player_kyo.x > 1230:
            self.player_kyo.x = 1230

        if self.jump_frame >= 12:
            self.player_kyo.y = 200
            self.player_kyo.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.player_kyo.face_dir == 1:
            self.player_kyo.image.clip_composite_draw(87 * int(self.jump_frame), 0, 87, 183, 0, 'h',
                                                     self.player_kyo.x, self.player_kyo.y, 180, 600)
        else:
            self.player_kyo.image.clip_composite_draw(87 * int(self.jump_frame), 0, 87, 183, 0, '0',
                                                     self.player_kyo.x, self.player_kyo.y, 180, 600)

class Run:
    def __init__(self, kyo):
        self.player_kyo = kyo
        self.run_frame = 0

    def enter(self, e):
        self.run_frame = 0
        if self.player_kyo.face_dir == 1:
            if right_down(e):
                self.player_kyo.dir = 1
                self.player_kyo.load_image(f'kyo_backwalk_sprite.png')
            elif left_down(e):
                self.player_kyo.dir = -1
                self.player_kyo.load_image(f'kyo_walk_sprite.png')
        else:
            if right_down(e):
                self.player_kyo.dir = -1
                self.player_kyo.load_image(f'kyo_walk_sprite.png')
            elif left_down(e):
                self.player_kyo.dir = 1
                self.player_kyo.load_image(f'kyo_backwalk_sprite.png')

    def exit(self, e):
        pass

    def do(self):
        self.run_frame = (self.run_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        if self.player_kyo.face_dir == 1:
            if self.player_kyo.dir == -1:
                self.player_kyo.load_image(f'kyo_walk_sprite.png')
            else:
                self.player_kyo.load_image(f'kyo_backwalk_sprite.png')
        else:
            if self.player_kyo.dir == -1:
                self.player_kyo.load_image(f'kyo_backwalk_sprite.png')
            else:
                self.player_kyo.load_image(f'kyo_walk_sprite.png')

        self.player_kyo.x += self.player_kyo.dir * RUN_SPEED_PPS * game_framework.frame_time
        if self.player_kyo.x < 50:
            self.player_kyo.x = 5
        elif self.player_kyo.x > 1230:
            self.player_kyo.x = 1230

    def draw(self):
        if self.player_kyo.face_dir == 1:
            if self.player_kyo.dir == -1:
                self.player_kyo.image.clip_composite_draw(63 * int(self.run_frame), 0, 63, 118, 0, 'h',
                                                         self.player_kyo.x, self.player_kyo.y, 150, 320)
            else:
                self.player_kyo.image.clip_composite_draw(58 * int(self.run_frame), 0, 58, 118, 0, 'h',
                                                         self.player_kyo.x, self.player_kyo.y, 150, 320)
        else:
            if self.player_kyo.dir == 1:
                self.player_kyo.image.clip_composite_draw(63 * int(self.run_frame), 0, 63, 118, 0, '',
                                                         self.player_kyo.x, self.player_kyo.y, 150, 320)
            else:
                self.player_kyo.image.clip_composite_draw(58 * int(self.run_frame), 0, 58, 118, 0, '',
                                                         self.player_kyo.x, self.player_kyo.y, 150, 320)

class Idle:
    def __init__(self, kyo):
        self.player_kyo = kyo
        self.idle_frame = 0

    def enter(self, e):
        self.player_kyo.dir = 0
        self.player_kyo.load_image(f'kyo_idle_sprite.png')
        self.idle_frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.idle_frame = (self.idle_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time*1.5) % 10

    def draw(self):
        if self.player_kyo.face_dir == 1:
            self.player_kyo.image.clip_composite_draw(64 * int(self.idle_frame), 0, 64, 106, 0, 'h',
                                                     self.player_kyo.x, self.player_kyo.y,150,300)
        else:
            self.player_kyo.image.clip_composite_draw(64 * int(self.idle_frame), 0, 64, 106, 0, '',
                                                     self.player_kyo.x, self.player_kyo.y,150,300)

class Playerkyo:
    def __init__(self):
        self.x, self.y = 950, 200
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.load_image('kyo_idle_sprite.png')
        self.hp = 100
        self.hit = False
        self.prev_state = None
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
                            (lambda e: k_down(e) and skill1_command(e)): self.SKILL1,
                            (lambda e: j_down(e) and skill2_command(e)): self.SKILL2,
                            k_down: self.KICK, j_down: self.PUNCH},
                self.RUN: {right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE,
                           left_down: self.IDLE, up_down: self.JUMP, k_down: self.KICK, j_down: self.PUNCH},
                self.JUMP: {time_out: self.IDLE,
                            (lambda e, jj=self.JUMP: k_down(e) and jj.jump_frame < 7): self.JUMPKICK},
                self.JUMPKICK: {time_out: self.IDLE},
                self.KICK: {time_out: self.IDLE},
                self.PUNCH: {time_out: self.IDLE},
                self.SKILL1: {time_out: self.IDLE},
                self.SKILL2: {time_out: self.IDLE,}
            }
        )

    def load_image(self, path):
        self.image = load_resource(path)

    def update(self):
        current_state = self.state_machine.cur_state
        if self.prev_state != current_state:
            # 공격 상태로 전환될 때 hit 플래그 초기화
            if current_state in [self.KICK, self.PUNCH, self.JUMPKICK, self.SKILL1, self.SKILL2]:
                self.hit = False
            self.prev_state = current_state
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
        if self.face_dir == 1:
            if (self.state_machine.cur_state == self.IDLE or
                    self.state_machine.cur_state == self.RUN):
                return self.x - 40, self.y - 130, self.x + 55, self.y + 130
            elif self.state_machine.cur_state == self.JUMP:
                return self.x - 40, self.y + 20, self.x + 55, self.y + 280
            elif self.state_machine.cur_state == self.JUMPKICK:
                return self.x - 150, self.y + 70, self.x + 25, self.y + 130
            elif self.state_machine.cur_state == self.KICK:
                return self.x - 140, self.y + 30, self.x + 80, self.y + 90
            elif self.state_machine.cur_state == self.PUNCH:
                return self.x - 140, self.y + 10, self.x + 80, self.y + 70
            elif self.state_machine.cur_state == self.SKILL1:
                return self.x - 170, self.y - 70, self.x + 100, self.y + 230
            elif self.state_machine.cur_state == self.SKILL2:
                return self.x - 200, self.y + 35, self.x + 100, self.y + 300
        else:
            if (self.state_machine.cur_state == self.IDLE or
                    self.state_machine.cur_state == self.RUN):
                return self.x - 60, self.y - 130, self.x + 35, self.y + 130
            elif self.state_machine.cur_state == self.JUMP:
                return self.x - 60, self.y + 20, self.x + 35, self.y + 280
            elif self.state_machine.cur_state == self.JUMPKICK:
                return self.x - 50, self.y + 70, self.x + 145, self.y + 130
            elif self.state_machine.cur_state == self.KICK:
                return self.x - 40, self.y + 30, self.x + 140, self.y + 90
            elif self.state_machine.cur_state == self.PUNCH:
                return self.x - 40, self.y + 10, self.x + 140, self.y + 70
            elif self.state_machine.cur_state == self.SKILL1:
                return self.x - 70, self.y - 70, self.x + 170, self.y + 230
            elif self.state_machine.cur_state == self.SKILL2:
                return self.x - 100, self.y + 35, self.x + 200, self.y + 300

    def handle_collision(self, group, other):
        if group == 'r_vs_l':
            # 자신이 스킬 중무적
            if (self.state_machine.cur_state == self.SKILL1 or
                    self.state_machine.cur_state == self.SKILL2):
                return
            if other.hit:
                return
            # 상대방이 공격 중
            if (other.state_machine.cur_state == other.KICK or
                    other.state_machine.cur_state == other.PUNCH or
                    other.state_machine.cur_state == other.JUMPKICK or
                    other.state_machine.cur_state == other.SKILL1 or
                    other.state_machine.cur_state == other.SKILL2):

                # 상대방의 스킬 공격인지 확인
                if (other.state_machine.cur_state == other.SKILL1 or
                        other.state_machine.cur_state == other.SKILL2):
                    self.hp -= 30
                else:
                    self.hp -= 10
                other.hit = True