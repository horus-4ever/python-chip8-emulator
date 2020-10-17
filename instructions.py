"""
SETUP THE REGISTER SET AND THE INSTRUCTION SET OF THE VCPU
"""

from vmachine import InstructionSetMeta, opcode
import random


class opcode(opcode):
    def __eq__(self, value):
        return self._value == (value & self.__masks__["N"])


class InstructionSet(InstructionSetMeta, size=2):
    @opcode(0x00E0, "NNNN")
    def _00E0(vm, **kw):
        """
        CLS : clear the screen buffer.
        """
        vm._screen.clear_buffer()

    ##################################
    #           JUMPS
    ##################################

    @opcode(0x00EE, "NNNN")
    def _OOEE(vm, **kw):
        """
        RET : return from subroutine.
        """
        vm._cpu["PC"] = vm._cpu.stack_pop()
        vm._cpu._jmp = True

    @opcode(0x1000, "NAAA")
    def _1XXX(vm, *, A=None, **kw):
        """
        JMP AAA : jump at address AAA.
        """
        vm._cpu["PC"] = A
        vm._cpu._jmp = True

    @opcode(0x2000, "NAAA")
    def _2XXX(vm, *, A=None, **kw):
        """
        CALL AAA : call subroutine at address AAA.
        """
        vm._cpu.stack_push(vm._cpu["PC"]+2)
        vm._cpu["PC"] = A
        vm._cpu._jmp = True

    @opcode(0x3000, "NXKK")
    def _3XKK(vm, *, X=None, K=None, **kw):
        """
        SKP Vx, KK : skip next instruction if Vx == KK.
        """
        if vm._cpu[X] == K:
            vm._cpu["PC"] += 2

    @opcode(0x4000, "NXKK")
    def _4XKK(vm, *, X=None, K=None, **kw):
        """
        SKPN Vx, KK : skip next instruction if Vx != KK.
        """
        if vm._cpu[X] != K:
            vm._cpu["PC"] += 2
    
    @opcode(0x5000, "NXYN")
    def _5XY0(vm, *, X=None, Y=None, **kw):
        """
        SKP Vx, Vy : skip next instruction if Vx == Vy.
        """
        if vm._cpu[X] == vm._cpu[Y]:
            vm._cpu["PC"] += 2

    ##################################
    #           OPERATORS
    ##################################

    @opcode(0x6000, "NXKK")
    def _6XKK(vm, *, X=None, K=None, **kx):
        """
        LOAD Vx, KK : load KK to register Vx.
        """
        vm._cpu[X] = K

    @opcode(0x7000, "NXKK")
    def _7XKK(vm, *, X=None, K=None, **kw):
        """
        ADD Vx, KK : add KK to Vx. No carry flag.
        """
        vm._cpu[X] += K

    @opcode(0x8000, "NXYN")
    def _8XY0(vm, *, X=None, Y=None, **kw):
        """
        LOAD Vx, Vy : load Vy into Vx.
        """
        vm._cpu[X] = vm._cpu[Y]

    @opcode(0x8001, "NXYN")
    def _8XY1(vm, *, X=None, Y=None, **kw):
        """
        OR Vx, Vy : perform a binary or between Vx and Vy and store the result in Vx.
        """
        vm._cpu[X] |= vm._cpu[Y]

    @opcode(0x8002, "NXYN")
    def _8XY2(vm, *, X=None, Y=None, **kw):
        """
        AND Vx, Vy : perform a binary and between Vx and Vy and store the result in Vx.
        """
        vm._cpu[X] &= vm._cpu[Y]

    @opcode(0x8003, "NXYN")
    def _8XY3(vm, *, X=None, Y=None, **kw):
        """
        XOR Vx, Vy : perform a binary xor between Vx and Vy and store the result in Vx.
        """
        vm._cpu[X] ^= vm._cpu[Y]

    @opcode(0x8004, "NXYN")
    def _8XY4(vm, *, X=None, Y=None, **kw):
        """
        ADD Vx, Vy : add Vy to Vx. Set VF to 1 if there is a carry.
        """
        v0, v1 = vm._cpu[X], vm._cpu[Y]
        vm._cpu[X] = v0 + v1
        vm._cpu[15] = (v0 + v1) > 255

    @opcode(0x8005, "NXYN")
    def _8XY5(vm, *, X=None, Y=None, **kw):
        """
        SUB Vx, Vy : substract Vy from Vx. Set VF to 1 if carry.
        """
        v0, v1 = vm._cpu[X], vm._cpu[Y]
        vm._cpu[X] = v0 - v1
        vm._cpu[15] = v0 >= v1

    @opcode(0x8006, "NXYN")
    def _8X06(vm, *, X=None, **kw):
        """
        SHR Vx, 1 : store the least significant bit of Vx into VF, then shift Vx.
        """
        vm._cpu[15] = vm._cpu[X] & 0x0001
        vm._cpu[X] >>= 1

    @opcode(0x8007, "NXYN")
    def _8XY7(vm, *, X=None, Y=None, **kw):
        """
        SUB Vx, Vy : substract Vx from Vy. Set VF to 1 if carry.
        """
        v0, v1 = vm._cpu[X], vm._cpu[Y]
        vm._cpu[X] = v1 - v0
        vm._cpu[15] = v1 >= v0

    @opcode(0x800E, "NXYN")
    def _8X0E(vm, *, X=None, **kw):
        """
        SHL Vx, 1 : store the most significant bit of Vx into VF, then shift Vx.
        """
        vm._cpu[15] = (vm._cpu[X] & 0x80) >> 15
        vm._cpu[X] <<= 1

    @opcode(0x9000, "NXYN")
    def _9XY0(vm, *, X=None, Y=None, **kw):
        """
        SKP Vx, Vy : skip next instruction if Vx != Vy.
        """
        if vm._cpu[X] != vm._cpu[Y]:
            vm._cpu["PC"] += 2

    ##################################
    #           OTHERS
    ##################################

    @opcode(0xA000, "NAAA")
    def _AXXX(vm, *, A=None, **kw):
        """
        LOAD I, AAA : load address AAA into I.
        """
        vm._cpu["I"] = A

    @opcode(0xB000, "NAAA")
    def _BXXX(vm, *, A=None, **kw):
        """
        JMP V0 + AAA : jump at address V0 + AAA.
        """
        vm._cpu["PC"] = vm._cpu[0] + A
        vm._cpu._jmp = True

    @opcode(0xC000, "NXKK")
    def _CXKK(vm, *, X=None, **kw):
        """
        RND Vx : generate a random byte, and store it into Vx.
        """
        vm._cpu[X] = random.randrange(256)

    ##################################
    #           DRAW SPRITE
    ##################################

    @opcode(0xD000, "NXYA")
    def _DXYA(vm, *, X=None, Y=None, A=None, **kw):
        """
        DRW Vx, Vy, A : draw A bytes to screen at position X, Y. If any bit on the screen is modified, set VF to 1.
        """
        v0, v1 = vm._cpu[X], vm._cpu[Y]
        flag = 0
        for y in range(A):
            byte = vm._memory[vm._cpu["I"] + y]
            flag |= vm._screen.draw_byte((v0, v1 + y), byte)
        vm._cpu["VF"] = int(bool(flag))

    ##################################
    #           KEYBOARD
    ##################################

    @opcode(0xE09E, "NXNN")
    def _EX9E(vm, *, X=None, **kw):
        """
        SKP Vx : skip next instruction if key Vx is pressed.
        """
        if vm._keyboard.is_pressed(hex(vm._cpu[X])[2:]):
            vm._cpu["PC"] += 2

    @opcode(0xE0A1, "NXNN")
    def _EXA1(vm, *, X=None, **kw):
        """
        SKPN Vx : skip next instruction if key Vx is not pressed.
        """
        if not vm._keyboard.is_pressed(hex(vm._cpu[X])[2:]):
            vm._cpu["PC"] += 2

    ##################################
    #           OTHERS
    ##################################

    @opcode(0xF007, "NXYN")
    def _FX07(vm, *, X=None, **kw):
        """
        LOAD Vx, DT : load the delay timer into register Vx.
        """
        vm._cpu[X] = vm._cpu["DT"]
    
    @opcode(0xF00A, "NXYN")
    def _FX0A(vm, *, X=None, **kw):
        """
        WAIT Vx : wait for any key to be pressed, and load the result into register Vx.
        """
        key = vm._keyboard.wait_for()
        if key == -1:
            vm._cpu._jmp = True
        else:
            vm._cpu[X] = key

    @opcode(0xF015, "NXNN")
    def _FX15(vm, *, X=None, **kw):
        """
        LOAD DT, Vx : load Vx into the delay timer.
        """
        vm._cpu["DT"] = vm._cpu[X]

    @opcode(0xF018, "NXNN")
    def _FX18(vm, *, X=None, **kw):
        """
        LOAD ST, Vx : load Vx into the sound timer.
        """
        vm._cpu["ST"] = vm._cpu[X]
        
    @opcode(0xF01E, "NXNN")
    def _FX1E(vm, *, X=None, **kw):
        """
        ADD I, Vx : add Vx to I. No carry flag.
        """
        vm._cpu["I"] += vm._cpu[X]

    @opcode(0xF029, "NXNN")
    def _FX29(vm, *, X=None, **kw):
        """
        FONT I, Vx : load into I the address of the sprite corresponding to the hex value of Vx.
        """
        vm._cpu["I"] = vm._cpu[X] * 5

    @opcode(0xF033, "NXNN")
    def _FX33(vm, *, X=None, **kw):
        """
        STO Vx : store at address I to I+3 the decimal representation of Vx. Example : 253 = 2 * 100 + 5 * 10 + 3 * 1.
        """
        value = vm._cpu[X]
        vm._memory[vm._cpu["I"] + 2] = value % 10
        value //= 10
        vm._memory[vm._cpu["I"] + 1] = value % 10
        value //= 10
        vm._memory[vm._cpu["I"] + 0] = value
        
    @opcode(0xF055, "NXNN")
    def _FX55(vm, *, X=None, **kwargs):
        for i in range(X+1):
            vm._memory[vm._cpu["I"]+i] = vm._cpu[i]

    @opcode(0xF065, "NXNN")
    def _FX65(vm, *, X=None, **kwargs):
        for i in range(X+1):
            vm._cpu[i] = vm._memory[vm._cpu["I"]+i]
