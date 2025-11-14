from pico2d import *

import game_framework
import game_world
import play_mode

global character_index

# 초기 화면 구성
def init():
    global title
    global canvas_x, canvas_y
    canvas_x, canvas_y = 1280, 720

    title = load_image('title.png')

def render_world():
    title.draw(canvas_x // 2, canvas_y // 2)

def handle_events():
    global x, y
    global character_index

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()

        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_1:
                character_index = 1
                game_framework.change_mode(play_mode)
            elif event.key == SDLK_2:
                character_index = 2
                game_framework.change_mode(play_mode)
            elif event.key == SDLK_3:
                character_index = 3
                game_framework.change_mode(play_mode)
            elif event.key == SDLK_4:
                character_index = 4
                game_framework.change_mode(play_mode)
            elif event.key == SDLK_ESCAPE:
                game_framework.quit()



def update():
    game_world.update()


def draw():
    clear_canvas()
    render_world()
    update_canvas()


def finish():
    game_world.clear()

def pause(): pass
def resume(): pass