from ui_config import resource_path


class AudioPlayer:
    def __init__(self, filename, volume=10, max_volume=10):
        self.filename = filename
        self.max_volume = max_volume
        self.volume = int(volume)
        self._last_volume = int(volume) if int(volume) > 0 else int(max_volume)
        self._muted = self.volume == 0
        self._available = True
        self._error = None
        self._started = False
        self._pygame = None

    @property
    def available(self):
        return self._available

    @property
    def error(self):
        return self._error

    @property
    def is_muted(self):
        return self._muted

    def start(self):
        if self._started:
            return
        try:
            import pygame

            self._pygame = pygame
            pygame.mixer.init()
            audio_path = resource_path(self.filename)
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.set_volume(self._clamp(self.volume) / self.max_volume)
            pygame.mixer.music.play(loops=-1)
            self._started = True
        except Exception as exc:
            self._available = False
            self._error = exc

    def _clamp(self, value):
        value = int(round(value))
        if value < 0:
            return 0
        if value > self.max_volume:
            return self.max_volume
        return value

    def set_volume(self, value):
        value = self._clamp(value)
        self.volume = value
        if value == 0:
            self._muted = True
        else:
            self._muted = False
            self._last_volume = value
        if self._started:
            self._pygame.mixer.music.set_volume(value / self.max_volume)

    def toggle_mute(self):
        if self._muted:
            restore = self._last_volume if self._last_volume > 0 else self.max_volume
            self.set_volume(restore)
        else:
            if self.volume > 0:
                self._last_volume = self.volume
            self.set_volume(0)
