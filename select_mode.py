from pico2d import *

import game_framework
import game_world
import play_mode
from sound_manager import sound_manager

# 초기 화면 구성
def init():
    global title
    global canvas_x, canvas_y
    global font
    global character_index
    character_index = 1
    font = load_font('kof_font.TTF', 30)
    canvas_x, canvas_y = 1280, 720

    title = load_image('select.png')

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
            if event.key == SDLK_LEFT:  # '1' 키
                character_index -= 1
                sound_manager.play('button')
                if character_index < 1:
                    character_index = 4
            elif event.key == SDLK_RIGHT:  # '2' 키
                character_index += 1
                sound_manager.play('button')
                if character_index > 4:
                    character_index = 1
            elif event.key == SDLK_SPACE:
                game_framework.set_character_index(character_index)
                sound_manager.play('next_scene')
                game_framework.change_mode(play_mode)# 'SPACE' 키
            elif event.key == SDLK_ESCAPE:
                game_framework.quit()




def update():
    game_world.update()


def draw():
    clear_canvas()
    render_world()
    if character_index == 1:
        font.draw(100, 460, 'now', (255, 255, 0))
    elif character_index == 2:
        font.draw(390, 460, 'now', (255, 255, 0))
    elif character_index == 3:
        font.draw(685, 460, 'now', (255, 255, 0))
    elif character_index == 4:
        font.draw(970, 460, 'now', (255, 255, 0))
    font.draw(320, 600,'Select Your Character', (255, 0, 0))
    font.draw(260, 160, 'Press the space to select', (255, 0, 0))
    update_canvas()


def finish():
    game_world.clear()

def pause(): pass
def resume(): pass