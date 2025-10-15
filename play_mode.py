import random
from pico2d import *

import game_framework
import game_world

boy = None


def init():
    pass

def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()


def pause(): pass
def resume(): pass

