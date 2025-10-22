from pico2d import load_image, load_font, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_SPACE

import game_framework
import game_world

from state_machine import StateMachine

def space_down(e): # e is space down ?
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

class title:
    def __init__(self):
        self.image = load_image('title.png')

    def draw(self):
        self.image.clip_draw(0,0,1280,720,640,360)

    def exit(self,e):
        if space_down(e):
            quit()

    def handle_event(self,event):
        pass