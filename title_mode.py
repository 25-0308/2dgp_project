from pico2d import *

import game_framework
import game_world


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

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()

        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_SPACE:  # '=' 키
                pass
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