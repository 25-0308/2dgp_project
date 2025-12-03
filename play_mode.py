import random
from pico2d import *

import game_framework

from random import randint

from player_kk import Playerkk
from Player_iori import Playeriori
from player_kyo import Playerkyo
from player_mai import Playermai

import game_world
import ending_mode

global bg_timer
global bg_count

global font
global dead_flag
global fontsize
dead_flag = False

def handle_events():
    global dead_flag
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_m:
            dead_flag = True
        else:
            player_r.handle_event(event)

def init():
    global bg
    global bg_count
    global bg_timer
    bg_count = 0
    bg_timer = game_framework.frame_time

    global canvas_x, canvas_y
    canvas_x, canvas_y = 1280, 720

    bg = load_image(f'stage_{bg_count}.png')
    global player_r, player_l

    global font
    global fontsize
    font = load_font('kof_font.TTF', 30)
    fontsize = 0
    if game_framework.get_character_index() == 1:
        player_r = Playermai()
    elif game_framework.get_character_index() == 2:
        player_r = Playerkk()
    elif game_framework.get_character_index() == 3:
      player_r = Playerkyo()
    elif game_framework.get_character_index() == 4:
       player_r = Playeriori()

    index = randint(1,4)
    if index == 1:
        player_l = Playermai()
    elif index == 2:
        player_l = Playerkk()
    elif index == 3:
       player_l = Playerkyo()
    elif index == 4:
       player_l = Playeriori()

    player_r.face_dir = -1
    player_l.face_dir = 1
    player_r.x , player_r.y = 950, 200
    player_l.x , player_l.y = 330, 200

    game_world.add_object(player_r)
    game_world.add_object(player_l)

    game_world.add_collision_pair('r_vs_l',player_l,player_r)

def update():
    game_world.update()
    global bg_count
    global bg
    global bg_timer
    global fontsize

    bg_timer += game_framework.frame_time
    if bg_timer >= 0.15:
        bg_timer = 0.0
        bg_count += 1
    if dead_flag:
        fontsize += 50*game_framework.frame_time
        if(fontsize >=120):
            fontsize = 120

    bg = load_image(f'stage_{bg_count % 8}.png')
    game_world.handle_collisions()

def draw():
    global dead_flag
    global fontsize
    global font
    font = load_font('kof_font.TTF', int(fontsize))
    clear_canvas()
    bg.clip_composite_draw(0, 0, 752, 224, 0,'0',
                           canvas_x // 2, canvas_y // 2,canvas_x,canvas_y)
    if dead_flag:
        font.draw(canvas_x // 2 - 250, 550, 'K O!', (255, 255, 0))
    if fontsize == 120:
        delay(2.0)
        game_framework.change_mode(ending_mode)

    game_world.render()
    update_canvas()

def finish():
    game_world.clear()


def pause(): pass
def resume(): pass
