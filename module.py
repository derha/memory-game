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

# general functions and classes


def text_surface(digit, font_size=60, text_rgb=BLACK, bg_rgb=BLUE):
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
    NEWGAME = 1
    NEXT_LEVEL = 2
    INPUT = 3
    EVAL = 4
    END = 5


def game_loop(screen, buttons, obj=None, obj_pos=None):
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.fill(BLUE)
        if obj is not None:
            screen.blit(obj, obj_pos)

        for button in buttons:
            action = button.update(pygame.mouse.get_pos(), mouse_up)
            if action is not None:
                return action
        buttons.draw(screen)

        pygame.display.flip()


# functions for actual states


def title_screen(screen):
    start = Button(
        center_position=(400, 300),
        path_default=join("images", "icons", "start1.png"),
        path_highlighted=join("images", "icons", "start2.png"),
        action=State.NEWGAME
    )

    buttons = RenderUpdates(start)

    return game_loop(screen, buttons)


def display(screen, level, pattern):
    screen.fill(BLUE)
    screen.blit(text_surface("Level " + str(level)), (280, 250))
    pygame.display.flip()
    pygame.time.delay(1000)
    screen.fill(BLUE)
    screen.blit(text_surface("Level " + str(level), 30), (20, 20))
    pygame.display.flip()
    pygame.time.delay(2000)

    for digit in pattern:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        obj = text_surface(str(digit), 90)

        screen.fill(BLUE)
        screen.blit(text_surface("Level " + str(level), 30), (20, 20))
        screen.blit(obj, (randint(90, 620), randint(90, 420)))

        pygame.display.flip()
        pygame.time.delay(1000)

    return State.INPUT


def input_page(screen, inp):
    numbers = []
    x = 75
    for i in range(10):
        x += 60
        numbers.append(Button(
            center_position=(x, 300),
            path_default=join("images", "input", str(i) + "_1.png"),
            path_highlighted=join("images", "input", str(i) + "_2.png"),
            action=State.INPUT
        ))

    clear = Button(
        center_position=(325, 400),
        path_default=join("images", "input", "clear_1.png"),
        path_highlighted=join("images", "input", "clear_2.png"),
        action=State.INPUT
    )

    done = Button(
        center_position=(475, 400),
        path_default=join("images", "input", "done_1.png"),
        path_highlighted=join("images", "input", "done_2.png"),
        action=State.EVAL
    )

    obj = text_surface("".join(list(map(str, inp))), 30) if inp else None
    obj_rect = obj.get_rect(center=(400, 150)) if obj is not None else None

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.fill(BLUE)
        if obj is not None:
            screen.blit(obj, obj_rect)

        for i, number in enumerate(numbers):
            action = number.update(pygame.mouse.get_pos(), mouse_up)
            if action is not None:
                inp.append(i)
                return action

        action = clear.update(pygame.mouse.get_pos(), mouse_up)
        if action is not None:
            if inp:
                inp.pop()
            return action

        action = done.update(pygame.mouse.get_pos(), mouse_up)
        if action is not None:
            return action

        buttons = RenderUpdates(numbers + [clear, done])
        buttons.draw(screen)

        pygame.display.flip()


def end_screen(screen):
    close = Button(
        center_position=(500, 400),
        path_default=join("images", "icons", "exit1.png"),
        path_highlighted=join("images", "icons", "exit2.png"),
        action=State.QUIT
    )

    restart = Button(
        center_position=(300, 400),
        path_default=join("images", "icons", "restart1.png"),
        path_highlighted=join("images", "icons", "restart2.png"),
        action=State.NEWGAME
    )

    buttons = RenderUpdates(restart, close)
    img = pygame.image.load(join("images", "game_over.png"))
    img = pygame.transform.scale(img, (300, 300))

    return game_loop(screen, buttons, img, (250, 25))
