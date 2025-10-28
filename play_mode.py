import random
from pico2d import *

import game_framework
import game_world

global bg_timer

global bg_count
global p_l_count

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

def init():
    global bg
    global bg_count
    global bg_timer
    global p_l_count
    bg_count = 0
    p_l_count = 0
    bg_timer = game_framework.frame_time

    global canvas_x, canvas_y
    canvas_x, canvas_y = 1280, 720

    bg = load_image(f'stage_{bg_count}.png')

    global player_l
    player_l = load_image(f'kk_{p_l_count}.png')

def update():
    game_world.update()
    global bg_count
    global p_l_count
    global player_l
    global bg
    global bg_timer

    bg_timer += game_framework.frame_time
    if bg_timer >= 0.15:
        bg_timer = 0.0
        bg_count += 1
        p_l_count += 1

    bg = load_image(f'stage_{bg_count % 8}.png')
    player_l = load_image(f'kk_{p_l_count % 4}.png')
    game_world.handle_collisions()

def draw():
    clear_canvas()
    bg.clip_composite_draw(0, 0, 752, 224, 0,'0',
                           canvas_x // 2, canvas_y // 2,canvas_x,canvas_y)
    player_l.clip_composite_draw(0,0,128,224,0,'0',900,200,200,300)
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()


def pause(): pass
def resume(): pass
