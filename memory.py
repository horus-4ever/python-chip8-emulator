from vmachine import Memory


class MemoryMap:
    SIZE = 4096
    OFFSET = 0x200
    SS = 4096 - 256


class VMemory(Memory):
    SIZE = MemoryMap.SIZE