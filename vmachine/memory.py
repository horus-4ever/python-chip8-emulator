class Memory:
    def __init__(self):
        self._memory = bytearray(self.__class__.SIZE)

    def store(self, address, bytes_):
        if address < 0:
            raise ValueError()
        for i, byte in enumerate(bytes_):
            self._memory[address + i] = byte

    def __getitem__(self, index):
        return self._memory[index]

    def __setitem__(self, index, value):
        self._memory[index] = value