import pygame


SCREEN_SIZE = (64, 32)
PIXEL_SIZE = 15
SCREEN_TOTAL_SIZE = (SCREEN_SIZE[0] * PIXEL_SIZE, SCREEN_SIZE[1] * PIXEL_SIZE)


class VScreen():
    def __init__(self, vm, size, surface):
        self._vm = vm
        self._size = size
        self._buffer = [[0 for _ in range(self._size[0])] for _ in range(self._size[1])]
        self._surface = surface

    def __next__(self):
        pass

    def refresh(self):
        self._surface.fill((0, 0, 0))
        for y, line in enumerate(self._buffer):
            for x, value in enumerate(line):
                if value == 0:
                    continue
                pygame.draw.rect(
                    self._surface,
                    (255, 255, 255),
                    (x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
                )
        pygame.display.flip()

    def clear_buffer(self):
        self._buffer = [[0 for _ in range(self._size[0])] for _ in range(self._size[1])]
        self.refresh()

    def draw_byte(self, position, value):
        x, y = position
        flag = False
        for i in range(8):
            # this 'if' checks if a pixel changed while drawing
            try:
                if self._buffer[y][x + i] and int(bool(value & (1 << (7 - i)))):
                    flag = True
                self._buffer[y][x + i] ^= int(bool(value & (1 << (7 - i))))
            except:
                pass
        self.refresh()
        return flag
