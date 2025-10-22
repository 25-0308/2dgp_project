from pico2d import open_canvas, close_canvas
import game_framework

import title_mode as title_mode

open_canvas(1280, 720)
game_framework.run(title_mode)
close_canvas()

