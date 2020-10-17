from instructions import InstructionSet
from registers import RegisterSet
from keyboard import KEY_MAP
from screen import SCREEN_SIZE, SCREEN_TOTAL_SIZE
from vm import VirtualMachine

import pygame
import sys
import os



if __name__ == "__main__":
    PATH = os.path.dirname(__file__)
    # get the code
    filename = os.path.join(PATH, sys.argv[1])
    with open(filename, "rb") as document:
        raw_code = document.read()
    # initialise the window
    display = pygame.display.set_mode(SCREEN_TOTAL_SIZE)
    # setup the vm
    vm = VirtualMachine(
        screen_size=SCREEN_SIZE, screen_surface=display,    # screen
        instruction_set=InstructionSet, register_set=RegisterSet(),   # cpu
        key_map=KEY_MAP # keyboard
    )
    vm.load(raw_code)
    # pygame event loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        next(vm)