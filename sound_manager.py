# sound_manager.py
from pico2d import load_wav

class SoundManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SoundManager, cls).__new__(cls)
            # 사운드를 저장할 딕셔너리 초기화
            cls._instance.sounds = {}
        return cls._instance

    def load(self, name, file_path):
        if name not in self.sounds:
            self.sounds[name] = load_wav(file_path)
            print(f'[SoundManager] Loaded: {name} from {file_path}')

    def play(self, name):
        if name in self.sounds:
            # 볼륨 조절이 필요하다면 self.sounds[name].set_volume(64) 와 같이 사용 (0~128)
            self.sounds[name].play()
        else:
            print(f'[SoundManager] Warning: Sound not found - {name}')

sound_manager = SoundManager()
