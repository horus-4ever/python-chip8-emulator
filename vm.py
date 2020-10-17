from keyboard import VKeyboard
from vcpu import VCPU
from screen import VScreen
from memory import VMemory, MemoryMap
from fonts import FONTS
import time



class VirtualMachine:

    CLOCK_FPS = 500

    def __init__(self, **kwargs):
        self._cpu = VCPU(self, kwargs["register_set"], kwargs["instruction_set"])
        self._screen = VScreen(self, kwargs["screen_size"], kwargs["screen_surface"])
        self._keyboard = VKeyboard(self, kwargs["key_map"])
        self._memory = VMemory()

    def load(self, raw_code):
        self._code = raw_code
        self._memory.store(MemoryMap.OFFSET, raw_code)
        self._memory.store(0, FONTS)
        self._cpu["PC"] = MemoryMap.OFFSET
        self._cpu["SP"] = MemoryMap.SIZE
        # print(self._memory._memory)

    def __next__(self):
        next(self._cpu)
        next(self._screen)
        time.sleep(1 / self.__class__.CLOCK_FPS)
