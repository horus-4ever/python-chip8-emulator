class VirtualCPU():
    def __init__(self, register_set, instruction_set):
        # cpu caracterisitcs : register set and instruction set
        self._register_set = register_set
        self._instruction_set = instruction_set

    def __next__(self):
        raise NotImplementedError()