#!/usr/bin/env python3
"""
An implementation of a NES simulator using Pygame.
"""

from __future__ import division
import sys
import pygame


class NesSimulator(object):
    """
    A class representing a NES simulator.

    Attributes:
        width (int): The width of the screen.
        height (int): The height of the screen.
        screen (pygame.Surface): The Pygame surface representing the screen.
        bg_color (tuple): The background color of the screen in RGB format.
        text (pygame.Surface): The rendered text that should appear on the screen.
        fps (int): The frames per second of the simulator.
        refresh (int): The Pygame event for refreshing the screen.
    """

    def __init__(self):
        """
        Initializes the NES simulator.
        """

        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.bg_color = 0, 0, 0
        font = pygame.font.Font("DejaVuSansMono.ttf", 100)
        self.text = font.render("text that should appear", True, (238, 58, 140))

        self.fps = 30
        self.refresh = pygame.USEREVENT + 1
        pygame.time.set_timer(self.refresh, 1000 // self.fps)

    def run(self):
        """
        Runs the NES simulator.
        """

        running = True
        while running:
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                running = False

            elif event.type == self.refresh:
                self.draw()

            else:
                pass

    def draw(self):
        """
        Draws the screen of the NES simulator.
        """

        self.screen.fill(self.bg_color)

        self.screen.blit(self.text, [400, 300])

        pygame.display.flip()


NesSimulator().run()
pygame.quit()
sys.exit()
