#!/usr/bin/env python3
"""
An implementation of a NES simulator using Pygame.
"""

from typing import Dict, List
import sys
import pygame


class HexdumpViewer:
    """
    A class for viewing hex dumps.

    Attributes:
        hex_dump (dict): A dictionary containing the hex dump data.
    """

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font_size = 14
        self.line_spacing = 28
        self.hex_dump : Dict[int, List[int]] = {
            0x0000 : [0x73, 0x72, 0x64, 0x3d, 0x34, 0x34, 0x34, 0x62, 0x3d, 0x34, 0x34, 0x34, 0x64, 0x33, 0x3d, 0x33],
            0x0010 : [0x64, 0x6b, 0x3d, 0x34, 0x34, 0x34, 0x64, 0x25, 0x56, 0x3d, 0x44, 0x34, 0xe4, 0x64, 0x3f, 0xc2],
            0x0020 : [0x6b, 0x3d, 0x2e, 0x2e, 0x0a, 0x69, 0x6c, 0x86, 0x3d, 0x34, 0x34, 0x34, 0x74, 0x74, 0x73, 0x65],
            0x0030 : [0x2e, 0x2e, 0x0a, 0x78, 0x65, 0x74, 0x6f, 0x67, 0x3d, 0x2e, 0x2e, 0x0a, 0x79, 0x6d, 0x6e, 0x73],
            0x0040 : [0x6f, 0x70, 0x3d, 0x2e, 0x2e, 0x0a, 0x6e, 0x63, 0x6f, 0x6c, 0x6f, 0x72, 0x3d, 0x32, 0x35, 0x36],
            0x0050 : [0x6e, 0x69, 0x3d, 0x34, 0x34, 0x34, 0x64, 0x6f, 0x3d, 0x34, 0x34, 0x34, 0x64, 0x6f, 0x3d, 0x34],
            0x0060 : [0x74, 0x3d, 0x2e, 0x33, 0x34, 0x6d, 0x72, 0x54, 0x3d, 0x34, 0x31, 0x2e, 0x30, 0x2e, 0x62, 0x0a],
            0x0070 : [0x74, 0x2d, 0x74, 0x70, 0x3d, 0x33, 0x30, 0x30, 0x2f, 0x73, 0x3d, 0x33, 0x30, 0x30, 0x2f, 0x73],
            0x0080 : [0x6d, 0x63, 0x62, 0x3d, 0x30, 0x3a, 0x34, 0x6d, 0x6b, 0x74, 0x3d, 0x2e, 0x2e, 0x0a, 0x6c, 0x6f],
            0x0090 : [0x75, 0x6c, 0x3d, 0x2e, 0x2e, 0x0a, 0x74, 0x79, 0x6d, 0x6e, 0x73, 0x3d, 0x2e, 0x2e, 0x0a, 0x4d],
            0x00a0 : [0x64, 0x74, 0x6e, 0x69, 0x6f, 0x3d, 0x34, 0x30, 0x2e, 0x0a, 0x4d, 0x64, 0x74, 0x6e, 0x69, 0x6f],
            0x00b0 : [0x34, 0x74, 0x63, 0x64, 0x69, 0x64, 0x3d, 0x34, 0x30, 0x2e, 0x0a, 0x4d, 0x64, 0x74, 0x6e, 0x69],
            0x00c0 : [0x34, 0x74, 0x74, 0x73, 0x65, 0x3d, 0x34, 0x31, 0x2e, 0x0a, 0x4d, 0x64, 0x74, 0x6e, 0x69, 0x34],
            0x00d0 : [0x2e, 0x0a, 0x6c, 0x74, 0x6f, 0x6d, 0x69, 0x73, 0x3d, 0x34, 0x34, 0x34, 0x74, 0x6b, 0x74, 0x3d],
            0x00e0 : [0x3d, 0x2e, 0x2e, 0x0a, 0x6c, 0x67, 0x79, 0x3d, 0x34, 0x34, 0x34, 0x74, 0x6b, 0x74, 0x3d, 0x3d],
            0x00f0 : [0x2e, 0x2e, 0x0a, 0x79, 0x6d, 0x6e, 0x73, 0x3d, 0x2e, 0x2e, 0x0a, 0x6f, 0x6d, 0x3d, 0x34, 0x34],
            0x0100 : [0x2e, 0x37, 0x34, 0x74, 0x6c, 0x6e, 0x3d, 0x33, 0x34, 0x74, 0x6e, 0x5f, 0x78, 0x65, 0x74, 0x6f],
            0x0110 : [0x34, 0x34, 0x74, 0x74, 0x73, 0x3d, 0x34, 0x31, 0x2e, 0x0a, 0x6f, 0x6d, 0x3d, 0x34, 0x34, 0x34],
            0x0120 : [0x34, 0x74, 0x63, 0x3d, 0x34, 0x2e, 0x2e, 0x0a, 0x6f, 0x6d, 0x3d, 0x34, 0x34, 0x34, 0x74, 0x6d],
            0x0130 : [0x6f, 0x6d, 0x3d, 0x34, 0x34, 0x34, 0x74, 0x6d, 0x6f, 0x6d, 0x3d, 0x34, 0x34, 0x34, 0x74, 0x6d],
            0x0140 : [0x6b, 0x74, 0xdd, 0x2e, 0x32, 0x34, 0x74, 0x70, 0x3d, 0x33, 0x30, 0x30, 0x2f, 0x73, 0x3d, 0x33],
            0x0150 : [0x6e, 0x5f, 0x78, 0x65, 0x74, 0x6f, 0x74, 0x3d, 0x2e, 0x33, 0x34, 0x6d, 0x72, 0x54, 0x3d, 0x34],
            0x0160 : [0x2e, 0x0a, 0x6c, 0x74, 0x6f, 0x6d, 0x69, 0x73, 0x3d, 0x34, 0x34, 0x34, 0x74, 0x6b, 0x74, 0x3d]
        }
        self.text_objects = []
        self.hexdump_str_y_position = []
        
    def create(self) -> None:
        """
        Draws the hex dump.
        """
        font = pygame.font.Font("DejaVuSansMono.ttf", self.font_size)
        for key, value in self.hex_dump.items():
            vals = " ".join([f"{val:02x}" for val in value])
            text = font.render(f"0x{key:04x}: {vals}", True, (238, 58, 140))
            self.text_objects.append(text)
            
    def blit(self) -> None:
        """
        Blits the hex dump to the screen.
        """
        add_extra = 0
        for i, text in enumerate(self.text_objects):
            if i % 8 == 0 and i != 0:
                # Add extra spacing for every 8 lines
                add_extra = (i/8)*16
            if i == 0:
                self.screen.blit(text, [10, 13])
                self.hexdump_str_y_position.append(13+1)
            else:
                next_line_pos = self.line_spacing + ((i-1)* 16) + add_extra
                self.hexdump_str_y_position.append(next_line_pos +1)
                self.screen.blit(text, [10, next_line_pos])


    # def update(self):
    #     pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(30, 30, 60, 60))
        
    def draw_rect_alpha(self, ):
        rect = pygame.Rect(30, self.hexdump_str_y_position[1], 40, 14)
        shape_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, (255,0,0, 150), shape_surf.get_rect())
        self.screen.blit(shape_surf, rect)
    

class NesSimulator:
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
        self.font_size = 16
        self.test_val = 20
        self.line_spacing = 28
        self.r_is_pressed = False
        # font = pygame.font.Font("DejaVuSansMono.ttf", self.font_size)
        # self.sample_text = "0000000 7361 7274 696f 3d64 333d 312e 302e 620a"
        # self.text0 = font.render(self.sample_text, True, (238, 58, 140))
        # self.text1 = font.render(self.sample_text, True, (238, 58, 140))
        
        self.hex_dumper = HexdumpViewer(self.screen)
        self.hex_dumper.create()

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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    self.test_val += 1
                    print("test_val: ", self.test_val)
                    # font = pygame.font.Font("DejaVuSansMono.ttf", self.font_size)
                    # self.text0 = font.render("sdfsdsd sf sdf sd fs df sdf ", True, (238, 58, 140))
                    #self.text1 = font.render(self.sample_text, True, (238, 58, 140))
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    self.test_val -= 1
                    print("test_val: ", self.test_val)
                    #font = pygame.font.Font("DejaVuSansMono.ttf", self.font_size)
                    #self.text0 = font.render(self.sample_text, True, (238, 58, 140))
                    #self.text1 = font.render(self.sample_text, True, (238, 58, 140))
                elif event.key == pygame.K_r:
                    print("r presed")
                    self.hex_dumper.update()
            else:
                pass

    def draw(self):
        """
        Draws the screen of the NES simulator.
        """

        self.screen.fill(self.bg_color)
        # pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(30, 30, 60, 60))
        #self.screen.blit(self.text0, [10, 10])
        self.hex_dumper.blit()
        self.hex_dumper.draw_rect_alpha()
        #self.screen.blit(self.text1, [10, self.line_spacing])
        pygame.display.flip()


NesSimulator().run()
pygame.quit()
sys.exit()
