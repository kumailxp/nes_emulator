#!/usr/bin/env python3
"""
An implementation of a NES simulator using Pygame.
"""

from typing import Dict, List
import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from nes.bus import Bus


class HexdumpViewer:
    """
    A class for viewing hex dumps.

    Attributes:
        hex_dump (dict): A dictionary containing the hex dump data.
    """

    def __init__(self, screen: pygame.Surface | None) -> None:
        if screen is None:
            return
        else:
            self.screen = screen
        self.font_size = 14
        self.line_spacing = 28
        self.hex_dump: Dict[int, List[int]] = {}
        for i in range(0x0000, 0x00080, 0x0010):
            self.hex_dump[i] = [0] * 16

        self.text_objects: Dict[int, pygame.Surface] = {}
        self.hexdump_str_y_position = []

        g = pygame.Color("green3")
        self.slider = Slider(
            screen,
            470,
            186,
            10,
            260,
            min=0,
            max=99,
            initial=99,
            step=1,
            handleRadius=10,
            vertical=True,
            handleColour=(g.r, g.g, g.b),
        )
        self.output = TextBox(screen, 475, 200, 50, 50, fontSize=30)

        self.simple_font = pygame.font.Font("DejaVuSansMono.ttf", self.font_size)
        self.bold_font = pygame.font.Font("DejaVuSansMono-Bold.ttf", self.font_size)

    def create(self) -> None:
        """
        Draws the hex dump.
        """
        self.text_objects.clear()
        for key, value in self.hex_dump.items():
            print(key, value)
            vals = " ".join([f"{val:02X}" for val in value])
            text = self.simple_font.render(
                f"0x{key:04X}: {vals}", True, pygame.Color("green1")
            )
            self.text_objects[key] = text

    def blit(self) -> None:
        """
        Blits the hex dump to the screen.
        """
        add_extra = 0
        self.screen: pygame.Surface
        inital_space = 24
        for i, (_, text) in enumerate(self.text_objects.items()):
            if i % 8 == 0 and i != 0:
                # Add extra spacing for every 8 lines
                add_extra = (i / 8) * 16

            next_line_pos = (
                self.line_spacing + (inital_space + ((i - 1) * 16)) + add_extra
            )
            self.hexdump_str_y_position.append(next_line_pos)
            self.screen.blit(text, [14, next_line_pos])

    def draw_rect_alpha(self):
        """
        Draws two semi-transparent rectangles on the screen.

        The rectangles are positioned at specific coordinates and have a size of 20x14 pixels.
        The color of the rectangles is red with an alpha value of 150 (semi-transparent).

        """
        rect = pygame.Rect(75 + (24 * 0), self.hexdump_str_y_position[1], 22, 17)
        shape_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            shape_surf, pygame.Color("yellow"), shape_surf.get_rect(), width=1
        )
        self.screen.blit(shape_surf, rect)

        rect = pygame.Rect(0, 0, 500, 465)
        shape_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            shape_surf, pygame.Color("white"), shape_surf.get_rect(), width=3
        )

        text = self.bold_font.render(
            " Hex Dump" + str(" " * 53), True, pygame.Color("black")
        )
        temp_surface = pygame.Surface(text.get_size())
        temp_surface.fill(pygame.Color("white"))
        temp_surface.blit(text, (0, 0))
        self.screen.blit(temp_surface, [3, 3])

        self.screen.blit(shape_surf, rect)
        self.output.setText(self.slider.getValue())

    def check_128_byte_chunk(self, chunk) -> bool:
        """
        Checks if the current chunk of data is 128 bytes.

        Returns:
            bool: True if the current chunk of data is 128 bytes, False otherwise.
        """
        assert len(chunk) == 128
        return all(chunk == 0 for chunk in chunk)

    def load_from_file(self, ram_offset_: int, file_path_: str) -> None:
        """
        Loads the hex dump from a file.

        Args:
            ram_offset_ (int): The offset in the emulator's memory where the hex dump
            should be loaded. file_path_ (str): The path to the file containing
            the hex dump.
        """
        nes = Bus()
        nes.load_to_ram(ram_offset_, file_path_)
        ram = nes.ram
        for offset in range(0, len(ram), 128):
            chunk = ram[offset : offset + 128]
            if not self.check_128_byte_chunk(chunk):
                sixteen_byte_chunks = HexdumpViewer.split_into_16_bytes(chunk)
                for byte_chunk in sixteen_byte_chunks:
                    self.hex_dump[offset] = byte_chunk
                    offset += 16
        self.create()

    def load(self, ram_offset_, asm_string_):
        """
        Load the given assembly code into the emulator's memory.

        Args:
            ram_offset_ (int): The offset in the emulator's memory where
            the assembly code should be loaded.
            asm_string_ (str): The assembly code to be loaded.

        """
        asm_list = HexdumpViewer.split_asm_hex_in_16(asm_string_)
        for i, byte_chunk in enumerate(asm_list):
            self.hex_dump[ram_offset_ + (i * 16)] = byte_chunk
        self.create()

    @classmethod
    def clean_up_string(cls, asm_string_: str) -> List[str]:
        """
        Cleans up the assembly string.

        Args:
            asm_string (str): The assembly string.

        Returns:
            List[str]: The cleaned up assembly string.
        """
        asm_string_ = asm_string_.replace("\n", " ")
        asm_list = asm_string_.split(" ")
        asm_list_clean = [val for val in asm_list if val != ""]
        return asm_list_clean

    @classmethod
    def split_asm_string_in_16(cls, asm_string_: str) -> List[List[str]]:
        """
        Splits an assembly string into a list of lists, each containing 16 elements.

        Args:
            asm_string (str): The assembly string to be split.

        Returns:
            List[List[str]]: A list of lists, where each inner list
            contains 16 elements from the original string.
        """
        asm_list = HexdumpViewer.clean_up_string(asm_string_)
        asm_list_split = [asm_list[i : i + 16] for i in range(0, len(asm_list), 16)]
        return asm_list_split

    @classmethod
    def split_asm_hex_in_16(cls, asm_string_: str) -> List[List[int]]:
        """
        Splits the given assembly string into a list of lists,
        where each inner list contains 16 hexadecimal values.

        Args:
            asm_string (str): The assembly string to be split.

        Returns:
            List[List[int]]: A list of lists, where each inner list
            contains 16 hexadecimal values.

        """
        asm_list = HexdumpViewer.clean_up_string(asm_string_)
        asm_list_in_hex = [(int(val, 16)) for val in asm_list]
        asm_list_in_hex_split = [
            asm_list_in_hex[i : i + 16] for i in range(0, len(asm_list_in_hex), 16)
        ]
        missing = 16 - len(asm_list_in_hex_split[-1])
        if missing:
            asm_list_in_hex_split[-1] += [0] * missing
        return asm_list_in_hex_split

    @classmethod
    def split_into_16_bytes(cls, hex_array):
        """
        Splits the given list of hexadecimal values into a list of lists,
        where each inner list contains 16 hexadecimal values.

        Args:
            hex_array (List[int]): The list of hexadecimal values to be split.

        Returns:
            List[List[int]]: A list of lists, where each inner list contains 16 hexadecimal values.

        """
        temp = [hex_array[i : i + 16] for i in range(0, len(hex_array), 16)]
        hex_array_split = []
        for bytes_chunk in temp:
            t = []
            for byte in bytes_chunk:
                t.append(int(byte))
            hex_array_split.append(t)
        return hex_array_split


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
        pygame.display.set_caption("NES Simulator")
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
        # self.hex_dumper.create()
        ram_offset = 0x8000
        # asm_string = """
        # A2 0A 8E 00 00 A2 03 8E
        # 01 00 AC 00 00 A9 00 18
        # 6D 01 00 88 D0 FA 8D 02
        # 00 EA EA EA
        # """
        self.hex_dumper.load_from_file(ram_offset, "nestest.nes")

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
                    # self.text1 = font.render(self.sample_text, True, (238, 58, 140))
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    self.test_val -= 1
                    print("test_val: ", self.test_val)
                    # font = pygame.font.Font("DejaVuSansMono.ttf", self.font_size)
                    # self.text0 = font.render(self.sample_text, True, (238, 58, 140))
                    # self.text1 = font.render(self.sample_text, True, (238, 58, 140))
                elif event.key == pygame.K_r:
                    print("r presed")
                    # self.hex_dumper.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("Mouse button pressed")
                print(
                    "Position:", event.pos
                )  # event.pos is a tuple (x, y) representing the
            else:
                pass

            pygame_widgets.update(event)
            pygame.display.update()

    def draw(self):
        """
        Draws the screen of the NES simulator.
        """

        self.screen.fill(self.bg_color)
        # pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(30, 30, 60, 60))
        # self.screen.blit(self.text0, [10, 10])
        self.hex_dumper.blit()
        self.hex_dumper.draw_rect_alpha()
        # self.screen.blit(self.text1, [10, self.line_spacing])
        pygame.display.flip()


if __name__ == "__main__":
    # x = HexdumpViewer(None)
    # x.load_from_file(0x0080, "6502-mult.bin")
    NesSimulator().run()
    pygame.quit()
