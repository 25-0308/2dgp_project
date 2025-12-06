from pico2d import *

import game_framework
import game_world
import play_mode
import select_mode

from sound_manager import sound_manager

global font

# 초기 화면 구성
def init():
    global title
    global canvas_x, canvas_y
    canvas_x, canvas_y = 1280, 720
    global winner_kk
    global winner_iori
    global winner_kyo
    global winner_mai
    global winner_index

    global font
    font = load_font('kof_font.TTF', 80)

    title = load_image('stage_0.png')
    winner_kk = load_image('kk_win.png')
    winner_iori = load_image('iori_win.png')
    winner_kyo = load_image('kyo_win.png')
    winner_mai = load_image('mai_win.png')
    sound_manager.play('winner',50)
    if play_mode.winner_index == 1:
        sound_manager.play('mai_victory',50)
    elif play_mode.winner_index == 2:
        sound_manager.play('kk_victory',50)
    elif play_mode.winner_index == 3:
        sound_manager.play('kyo_victory',50)
    elif play_mode.winner_index == 4:
        sound_manager.play('iori_victory',50)

def render_world():
    global font
    title.clip_composite_draw(0,0,752,224,0,'0',
                              canvas_x // 2, canvas_y // 2,canvas_x,canvas_y)
    winner_index = play_mode.winner_index
    if winner_index == 1:
        winner_mai.clip_composite_draw(0,0,848,684,0,'0',
                              canvas_x // 2, canvas_y // 2 - 120,canvas_x // 3 * 2, canvas_y // 3 * 2)
    elif winner_index == 2:
        winner_kk.clip_composite_draw(0, 0, 640, 652, 0, '0',
                                   canvas_x // 2, canvas_y // 2 - 120, canvas_x // 3 * 2, canvas_y // 3 * 2)
    elif winner_index == 3:
        winner_kyo.clip_composite_draw(0, 0, 728, 652, 0, '0',
                                   canvas_x // 2, canvas_y // 2 - 120, canvas_x // 3 * 2, canvas_y // 3 * 2)
    elif winner_index == 4:
        winner_iori.clip_composite_draw(0, 0, 1160, 752, 0, '0',
                                   canvas_x // 2, canvas_y // 2 - 120, canvas_x // 3 * 2, canvas_y // 3 * 2)

    font.draw(canvas_x // 2 - 260, 600, 'WINNER!', (255, 255, 0))

def handle_events():
    global x, y

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()

        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
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