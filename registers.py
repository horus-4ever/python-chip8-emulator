from vmachine import _8BitRegister, _16BitRegister


class RegisterSet:
    # general purpose registers
    V0 = _8BitRegister()
    V1 = _8BitRegister()
    V2 = _8BitRegister()
    V3 = _8BitRegister()
    V4 = _8BitRegister()
    V5 = _8BitRegister()
    V6 = _8BitRegister()
    V7 = _8BitRegister()
    V8 = _8BitRegister()
    V9 = _8BitRegister()
    VA = _8BitRegister()
    VB = _8BitRegister()
    VC = _8BitRegister()
    VD = _8BitRegister()
    VE = _8BitRegister()
    VF = _8BitRegister()
    # timer and sound
    DT = _8BitRegister()
    ST = _8BitRegister()
    # others
    I = _16BitRegister()
    PC = _16BitRegister()
    SP = _16BitRegister()