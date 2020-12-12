#!/bin/bash

import pygame
from module import *
from random import randint


def main():
    pygame.init()

    window = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Memory Game")
    window.fill(BLUE)
    pygame.display.flip()

    level = 0
    pattern = []
    inp = []

    game_state = State.TITLE

    while True:
        if game_state == State.TITLE:
            game_state = title_screen(window)

        if game_state == State.NEWGAME:
            level = 1
            pattern = [randint(0, 9) for _ in range(4 + level)]
            inp = []
            game_state = display(window, level, pattern)

        if game_state == State.NEXT_LEVEL:
            level += 1
            pattern = [randint(0, 9) for _ in range(4 + level)]
            inp = []
            game_state = display(window, level, pattern)

        if game_state == State.INPUT:
            game_state = input_page(window, inp)

        if game_state == State.EVAL:
            game_state = State.NEXT_LEVEL if pattern == inp else State.END

        if game_state == State.END:
            game_state = end_screen(window)

        if game_state == State.QUIT:
            pygame.quit()
            return


if __name__ == '__main__':
    main()
