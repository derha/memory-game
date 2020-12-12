#!/bin/bash
import pygame
import pygame.freetype
from pygame.sprite import Sprite, RenderUpdates
from enum import Enum
from os.path import join
from random import randint
from sys import exit

BLUE = (102, 178, 255)
BLACK = (0, 0, 0)


def text_surface(digit, font_size=60, text_rgb=BLACK, bg_rgb=BLUE):
    """ Returns surface with text written on """
    font = pygame.freetype.SysFont("Consolas", font_size, bold=True)
    surface, _ = font.render(text=digit, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()


class Button(Sprite):
    def __init__(self, center_position, path_default, path_highlighted, action=None):
        super().__init__()

        self.mouse_over = False

        default_image = pygame.image.load(path_default)
        highlighted_image = pygame.image.load(path_highlighted)

        self.images = [default_image, highlighted_image]
        self.rects = [default_image.get_rect(center=center_position),
                      highlighted_image.get_rect(center=center_position)]

        self.action = action

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class State(Enum):
    QUIT = -1
    TITLE = 0
    INFO = 1
    NEWGAME = 2
    NEXT_LEVEL = 3
    END = 4


def game_loop(screen, buttons, image=None):
    img = None
    if image is not None:
        img = pygame.image.load(image)
        img = pygame.transform.scale(img, (300, 300))
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.fill(BLUE)
        if image is not None:
            screen.blit(img, (250, 25))

        for button in buttons:
            action = button.update(pygame.mouse.get_pos(), mouse_up)
            if action is not None:
                return action
        buttons.draw(screen)

        pygame.display.flip()


def title_screen(screen):
    start = Button(
        center_position=(400, 300),
        path_default=join("icons", "start1.png"),
        path_highlighted=join("icons", "start2.png"),
        action=State.NEWGAME
    )

    info = Button(
        center_position=(50, 50),
        path_default=join("icons", "info1.png"),
        path_highlighted=join("icons", "info2.png"),
        action=State.INFO
    )

    buttons = RenderUpdates(start, info)

    return game_loop(screen, buttons)


def info_page(screen):
    back = Button(
        center_position=(50, 50),
        path_default=join("icons", "back1.png"),
        path_highlighted=join("icons", "back2.png"),
        action=State.TITLE
    )

    buttons = RenderUpdates(back)

    return game_loop(screen, buttons)


def display(screen, level, pattern):
    screen.fill(BLUE)
    screen.blit(text_surface("Level " + str(level), 30), (20, 20))
    pygame.display.flip()
    pygame.time.delay(1000)
    for digit in pattern:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        obj = text_surface(str(digit))

        screen.fill(BLUE)
        screen.blit(text_surface("Level: " + str(level), 30), (20, 20))
        screen.blit(obj, (randint(50, 700), randint(50, 500)))

        pygame.display.flip()
        pygame.time.delay(1000)


def play(screen, level):
    pattern = []
    for i in range(4 + level):
        pattern.append(randint(0, 9))

    display(screen, level, pattern)
    # some more code for input
    return State.END


def end_screen(screen):
    close = Button(
        center_position=(500, 400),
        path_default=join("icons", "exit1.png"),
        path_highlighted=join("icons", "exit2.png"),
        action=State.QUIT
    )

    restart = Button(
        center_position=(300, 400),
        path_default=join("icons", "restart1.png"),
        path_highlighted=join("icons", "restart2.png"),
        action=State.NEWGAME
    )

    buttons = RenderUpdates(restart, close)

    return game_loop(screen, buttons, "game_over.png")