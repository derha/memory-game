#!/bin/bash

import pygame
from module import *
from os.path import join
from sys import exit
from random import randint
from time import sleep


def main():
    pygame.init()

    window = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Memory Game")
    window.fill(BLUE)
    pygame.display.flip()

    level = 0

    game_state = State.TITLE

    while True:
        if game_state == State.TITLE:
            game_state = title_screen(window)

        if game_state == State.INFO:
            game_state = info_page(window)

        if game_state == State.NEWGAME:
            level = 1
            game_state = play(window, level)

        if game_state == State.NEXT_LEVEL:
            level += 1
            game_state = play(window, level)

        if game_state == State.END:
            game_state = end_screen(window)

        if game_state == State.QUIT:
            pygame.quit()
            return


if __name__ == '__main__':
    main()
