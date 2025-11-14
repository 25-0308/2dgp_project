from pico2d import open_canvas, close_canvas
import game_framework

import title_mode
import select_mode
import play_mode
import ending_mode

open_canvas(1280, 720)
game_framework.run(select_mode)
close_canvas()