from vmachine import VirtualCPU


class VCPU(VirtualCPU):
    def __init__(self, vm, *args):
        # parent reference
        self._vm = vm
        self._jmp = False
        super().__init__(*args)

    def __next__(self):
        instruction = self.load_instruction()
        #print(hex(instruction))
        self._instruction_set.execute(self._vm, instruction)
        if not self._jmp:
            self["PC"] += 2
        self._jmp = False

        self._update_timers()

    def _update_timers(self):
        if self["DT"] > 0:
            self["DT"] -= 1
        if self["ST"] > 0:
            self["ST"] -= 1

    def __getitem__(self, key):
        if isinstance(key, str):
            return getattr(self._register_set, key)
        return getattr(self._register_set, f"V{hex(key).upper()[2:]}")

    def __setitem__(self, key, value):
        # print(vars(self._register_set))
        if isinstance(key, str):
            return setattr(self._register_set, key, value)
        return setattr(self._register_set, f"V{hex(key).upper()[2:]}", value)

    def stack_pop(self):
        self["SP"] += 2
        result = int.from_bytes(self._vm._memory[self["SP"] - 2: self["SP"]], "big")
        return result

    def stack_push(self, value):
        self["SP"] -= 2
        self._vm._memory[self["SP"]: self["SP"] + 2] = value.to_bytes(2, "big")

    def load_instruction(self):
        return int.from_bytes(self._vm._memory[self["PC"]: self["PC"] + 2], "big")
