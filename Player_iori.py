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
    abs_path = os.path.join(base_dir, 'iori', path)
    return load_image(abs_path)

# class Skill2:
#     def __init__(self, mai):
#         self.player_mai = mai
#         self.skill2_frame = 0
#
#     def enter(self, e):
#         self.player_mai.load_image('mai_skill2_sprite.png')
#         self.skill2_frame = 0
#         self.player_mai.y = 250
#
#     def exit(self, e):
#         self.player_mai.y = 200
#
#     def do(self):
#         self.skill2_frame = (self.skill2_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * 2.5) % 20
#         if self.skill2_frame >= 19:
#             self.player_mai.state_machine.handle_state_event(('TIMEOUT', None))
#
#     def draw(self):
#         if self.player_mai.face_dir == 1:
#             self.player_mai.image.clip_composite_draw(166*int(self.skill2_frame), 0, 166, 176, 0, 'h',
#                                                      self.player_mai.x, self.player_mai.y,360,420)
#         else:
#             self.player_mai.image.clip_composite_draw(166*int(self.skill2_frame), 0, 166, 176, 0, '0',
#                                                      self.player_mai.x, self.player_mai.y,360,420)
#
# class Skill1:
#     def __init__(self, mai):
#         self.player_mai = mai
#         self.skill1_frame = 0
#
#     def enter(self, e):
#         self.player_mai.load_image('mai_skill1_sprite.png')
#         self.skill1_frame = 0
#
#     def exit(self, e):
#         self.player_mai.y = 200
#
#     def do(self):
#         self.skill1_frame = (self.skill1_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * 3) % 18
#         if self.skill1_frame >= 17:
#             self.player_mai.state_machine.handle_state_event(('TIMEOUT', None))
#
#     def draw(self):
#         if self.player_mai.face_dir == 1:
#             self.player_mai.image.clip_composite_draw(177*int(self.skill1_frame), 0, 177, 114, 0, 'h',
#                                                      self.player_mai.x, self.player_mai.y,400,320)
#         else:
#             self.player_mai.image.clip_composite_draw(177*int(self.skill1_frame), 0, 177, 114, 0, '0',
#                                                      self.player_mai.x, self.player_mai.y,400,320)
#
# class Jumpkick:
#     def __init__(self, mai):
#         self.player_mai = mai
#         self.jumpkick_frame = 0
#
#     def enter(self, e):
#         global jumpattack_k_frame
#         self.player_mai.load_image('mai_jumpattack_sprite.png')
#         self.jumpkick_frame = jumpattack_k_frame
#
#     def exit(self, e):
#         self.player_mai.y = 200
#
#     def do(self):
#         self.jumpkick_frame = (self.jumpkick_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * 2.5) % 14
#         if self.jumpkick_frame >= 13:
#             self.player_mai.state_machine.handle_state_event(('TIMEOUT', None))
#
#     def draw(self):
#         if self.player_mai.face_dir == 1:
#             self.player_mai.image.clip_composite_draw(140*int(self.jumpkick_frame), 0, 140, 209, 0, 'h',
#                                                      self.player_mai.x, self.player_mai.y,350,500)
#         else:
#             self.player_mai.image.clip_composite_draw(140*int(self.jumpkick_frame), 0, 140, 209, 0, '0',
#                                                      self.player_mai.x, self.player_mai.y,350,500)
#
# class Punch:
#     def __init__(self, mai):
#         self.player_mai = mai
#         self.punch_frame = 0
#
#     def enter(self, e):
#         self.punch_frame = 0
#
#     def exit(self, e):
#         pass
#
#     def do(self):
#         self.punch_frame = (self.punch_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * 1.5) % 6
#         self.player_mai.load_image(f'mai_punch_{int(self.punch_frame)}.png')
#         if self.punch_frame >= 5:
#             self.player_mai.state_machine.handle_state_event(('TIMEOUT', None))
#
#     def draw(self):
#         if self.player_mai.face_dir == 1:
#             self.player_mai.image.clip_composite_draw(0, 0, 163, 119, 0, 'h',
#                                                      self.player_mai.x, self.player_mai.y,380,320)
#         else:
#             self.player_mai.image.clip_composite_draw(0, 0, 163, 119, 0, '0',
#                                                      self.player_mai.x, self.player_mai.y,380,320)
#
# class Kick:
#     def __init__(self, mai):
#         self.player_mai = mai
#         self.kick_frame = 0
#
#     def enter(self, e):
#         self.kick_frame = 0
#
#     def exit(self, e):
#         pass
#
#     def do(self):
#         self.kick_frame = (self.kick_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * 2) % 8
#         self.player_mai.load_image(f'mai_kick_{int(self.kick_frame)}.png')
#
#         if self.kick_frame >= 7:
#             self.player_mai.state_machine.handle_state_event(('TIMEOUT', None))
#
#     def draw(self):
#         if self.player_mai.face_dir == 1:
#             self.player_mai.image.clip_composite_draw(0, 0, 163, 119, 0, 'h',
#                                                      self.player_mai.x, self.player_mai.y,380,320)
#         else:
#             self.player_mai.image.clip_composite_draw(0, 0, 163, 119, 0, '0',
#                                                      self.player_mai.x, self.player_mai.y,380,320)
#
# class Jump:
#     def __init__(self, mai):
#         self.player_mai = mai
#         self.jump_frame = 0
#
#     def enter(self, e):
#         self.jump_frame = 0
#         self.player_mai.y = 350
#
#
#     def exit(self, e):
#         global  jumpattack_k_frame
#         self.player_mai.dir = 0
#         jumpattack_k_frame = self.jump_frame
#
#     def do(self):
#         self.jump_frame = (self.jump_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * 3) % 14
#
#         self.player_mai.load_image(f'mai_jump_sprite.png')
#
#         self.player_mai.x += self.player_mai.dir * RUN_SPEED_PPS * game_framework.frame_time
#
#         if self.player_mai.x < 50:
#             self.player_mai.x = 50
#         elif self.player_mai.x > 1230:
#             self.player_mai.x = 1230
#
#         if self.jump_frame >= 13:
#             self.player_mai.y = 200
#             self.player_mai.state_machine.handle_state_event(('TIMEOUT', None))
#
#     def draw(self):
#         if self.player_mai.face_dir == 1:
#             self.player_mai.image.clip_composite_draw(84 * int(self.jump_frame), 0, 84, 210, 0, 'h',
#                                                      self.player_mai.x, self.player_mai.y,180,600)
#         else:
#             self.player_mai.image.clip_composite_draw(84 * int(self.jump_frame), 0, 84, 201, 0, '0',
#                                                      self.player_mai.x, self.player_mai.y,180,600)
#
# class Run:
#     def __init__(self, mai):
#         self.player_mai = mai
#         self.run_frame = 0
#
#     def enter(self, e):
#         self.run_frame = 0
#         if self.player_mai.face_dir == 1:
#             if right_down(e):
#                 self.player_mai.dir = 1
#                 self.player_mai.load_image(f'mai_backwalk_{self.run_frame}.png')
#             elif left_down(e):
#                 self.player_mai.dir = -1
#                 self.player_mai.load_image(f'mai_walk_{self.run_frame}.png')
#         else:
#             if right_down(e):
#                 self.player_mai.dir = -1
#                 self.player_mai.load_image(f'mai_walk_{self.run_frame}.png')
#             elif left_down(e):
#                 self.player_mai.dir = 1
#                 self.player_mai.load_image(f'mai_backwalk_{self.run_frame}.png')
#
#
#     def exit(self, e):
#         pass
#
#     def do(self):
#         self.run_frame = (self.run_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
#         if self.player_mai.face_dir == 1:
#             if self.player_mai.dir == -1:
#                 self.player_mai.load_image(f'mai_walk_{int(self.run_frame)}.png')
#             else:
#                 self.player_mai.load_image(f'mai_backwalk_{int(self.run_frame)}.png')
#         else:
#             if self.player_mai.dir == 1:
#                 self.player_mai.load_image(f'mai_backwalk_{int(self.run_frame)}.png')
#             else:
#                 self.player_mai.load_image(f'mai_walk_{int(self.run_frame)}.png')
#
#         self.player_mai.x += self.player_mai.dir * RUN_SPEED_PPS * game_framework.frame_time
#         if self.player_mai.x < 50:
#             self.player_mai.x = 5
#         elif self.player_mai.x > 1230:
#             self.player_mai.x = 1230
#
#     def draw(self):
#         if self.player_mai.face_dir == 1:
#             if self.player_mai.dir == -1:
#                 self.player_mai.image.clip_composite_draw(0, 0, 73, 101, 0, 'h',
#                                                      self.player_mai.x, self.player_mai.y,200,300)
#             else:
#                 self.player_mai.image.clip_composite_draw(0, 0, 97, 104, 0, 'h',
#                                                      self.player_mai.x, self.player_mai.y,200,300)
#         else:
#             if self.player_mai.dir == 1:
#                 self.player_mai.image.clip_composite_draw(0, 0, 73, 101, 0, 'h',
#                                                      self.player_mai.x, self.player_mai.y,200,300)
#             else:
#                 self.player_mai.image.clip_composite_draw(0, 0, 97, 104, 0, 'h',
#                                                      self.player_mai.x, self.player_mai.y,200,300)

class Idle:
    def __init__(self, iori):
        self.player_iori = iori
        self.idle_frame = 0

    def enter(self, e):
        self.player_iori.dir = 0
        self.player_iori.load_image(f'iori_idle_sprite.png')
        self.idle_frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.idle_frame = (self.idle_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time*1.5) % 9

    def draw(self):
        if self.player_iori.face_dir == 1:
            self.player_iori.image.clip_composite_draw(74 * int(self.idle_frame), 0, 74, 102, 0, 'h',
                                                     self.player_iori.x, self.player_iori.y,180,300)
        else:
            self.player_iori.image.clip_composite_draw(74 * int(self.idle_frame), 0, 74, 102, 0, '',
                                                     self.player_iori.x, self.player_iori.y,180,300)

class Playeriori:
    def __init__(self):
        self.x, self.y = 950, 200
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.load_image('iori_idle_sprite.png')

        self.input_buffer = []

        self.IDLE = Idle(self)

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
                self.IDLE: {},
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