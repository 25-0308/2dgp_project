from pico2d import open_canvas, close_canvas
import game_framework
from sound_manager import sound_manager

import title_mode
import select_mode
import play_mode
import ending_mode
open_canvas(1280, 720)
sound_manager.load_all()
game_framework.run(title_mode)
close_canvas()