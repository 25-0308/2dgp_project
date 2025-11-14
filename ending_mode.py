from pico2d import *

import game_framework
import game_world
import play_mode

# 초기 화면 구성
def init():
    global title
    global canvas_x, canvas_y
    canvas_x, canvas_y = 1280, 720
    global winner_character

    title = load_image('stage_0.png')
    winner_character = load_image('kk_win.png')

def render_world():
    title.clip_composite_draw(0,0,752,224,0,'0',
                              canvas_x // 2, canvas_y // 2,canvas_x,canvas_y)
    winner_character.clip_composite_draw(0,0,640,652,0,'0',
                              canvas_x // 2, canvas_y // 2 - 120,canvas_x // 3 * 2, canvas_y // 3 * 2)

def handle_events():
    global x, y

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()

        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_SPACE:  # '=' 키
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