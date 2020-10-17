__all__ = ("Register", "_8BitRegister", "_16BitRegister", "_32BitRegister")

class Register:

    __slots__ = "_value",

    def __init__(self):
        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value % (2 ** self.__class__.SIZE)

    def __get__(self, instance, owner=None):
        return self.value

    def __set__(self, instance, value):
        self.value = value


class _8BitRegister(Register):
    SIZE = 8

class _16BitRegister(Register):
    SIZE = 16

class _32BitRegister(Register):
    SIZE = 32


