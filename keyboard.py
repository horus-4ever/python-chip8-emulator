import pygame
import time

KEY_MAP = {
    "1": "&", "2": "é", "3": "\"", "c": "'",
    "4": "a", "5": "z", "6": "e", "d": "r",
    "7": "q", "8": "s", "9": "d", "e": "f",
    "a": "w", "0": "x", "b": "c", "f": "v"
}

class VKeyboard():
    def __init__(self, vm, key_map):
        self._vm = vm
        self._key_map = key_map

    def is_pressed(self, key):
        keys = pygame.key.get_pressed()
        key = self._key_map[key]
        return keys[ord(key)]

    def wait_for(self):
        keyboard = pygame.key.get_pressed()
        for i, key in enumerate(keyboard):
            for k, v in self._key_map.items():
                if chr(i) == v and key:
                    return int(k, 16)
        return -1