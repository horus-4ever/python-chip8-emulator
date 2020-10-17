class opcode:

    __slots__ = ("_value", "_pattern", "_func", "__masks__")

    def __new__(cls, value, pattern):
        """opcode is a decorator. It takes two arguments :
        - value : it represents the instruction number.
        - pattern : it is a pattern to follow to decode the instruction easily. Masks are created from this pattern.

        Example : the insctruction 0x8001, which accepts two "arguments" 0x8XY1.
        - from this instruction, we can define the following pattern : "NXYN"
        - from this pattern, we can define 3 masks :
        -   - "N" : 0xF00F
        -   - "X" : 0x0F00
        -   - "Y" : 0x00F0
        While decoding an instruction, for instance 0x8231 :
        - "N" mask extracts the type of instruction : 0x8001
        - "X" mask extracts the first "argument" : 0x2
        - "Y" mask extracts the second "argument" : 0x3

        These decoding steps are implemented into "InstructionSetMeta".
        """
        self = super().__new__(cls)
        self._value = value
        self._pattern = pattern
        self.__masks__ = {}
        self.__offsets__ = {}
        # initialise the __masks__
        for i, letter in enumerate(reversed(pattern)):
            if letter in self.__masks__:
                self.__masks__[letter] |= 0xF << (4 * i)
            else:
                self.__masks__[letter] = 0xF << (4 * i)
                self.__offsets__[letter] = i
        # opcode is designed as a decorator
        def inner(func):
            self.__init__(func)
            return self
        return inner

    def __init__(self, func):
        self._func = func

    def __call__(self, vm, **kwargs):
        return self._func(vm, **kwargs)

    def __getattr__(self, name):
        return self.__masks__[name]

    def __eq__(self, _):
        """__eq__ must be defined by the user.
        It is part of the decoding process which can be found in "InstructionSetMeta".
        The purpose of __eq__ is here to check if an instruction is equal to an instruction type.
        """
        raise NotImplementedError()


class InstructionSetMeta:
    def __init_subclass__(subcls, size=4):
        subcls.__instruction_size__ = size

    @classmethod
    def find(cls, value):
        for _opcode in filter(lambda member: isinstance(member, opcode), cls.__dict__.values()):
            if _opcode == value:
                return _opcode
        raise KeyError(hex(value))

    @classmethod
    def execute(cls, vm, value):
        _opcode = cls.find(value)
        kwargs = {}
        for k, v in _opcode.__masks__.items():
            kwargs[k] = (value & v) >> (_opcode.__offsets__[k] * 4)
        return _opcode(vm, **kwargs)