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

    def __init__(
        self, screen: pygame.Surface | None, ram_offset_: int = 0, bin_len: int = 0
    ) -> None:
        if screen is None:
            return
        else:
            self.screen = screen

        self.ram_offset = ram_offset_
        self.hex_dump_line_spacing = 28
        self.hex_dump: Dict[int, List[int]] = {}
        for i in range(0x0000, 0x00080, 0x0010):
            self.hex_dump[i] = [0] * 16
        self.hex_lines: Dict[int, pygame.Surface] = {}
        self.hexdump_str_y_position = []

        self.font_size = 14
        self.simple_font = pygame.font.Font("DejaVuSansMono.ttf", self.font_size)
        self.bold_font = pygame.font.Font("DejaVuSansMono-Bold.ttf", self.font_size)
        self.simple_small_font = pygame.font.Font("DejaVuSansMono.ttf", 12)

        g = pygame.Color("green3")
        minv = (
            -self.ram_offset - (128 * 16)
            if bin_len == 0
            else -self.ram_offset - bin_len
        )
        self.hex_slider = Slider(
            screen,
            470,
            195,
            10,
            250,
            min=minv,
            max=-self.ram_offset,
            initial=0xFFFF,
            step=128,
            handleRadius=10,
            vertical=True,
            handleColour=(g.r, g.g, g.b),
        )

        self.hex_scroll_tooltip = TextBox(
            self.screen, 455, 160, 40, 24, font=self.simple_font, fontSize=12
        )
        self.hex_scroll_tooltip.disable()

        self.log_slider = Slider(
            screen,
            780,
            495,
            3,
            290,
            min=0,
            max=1000,
            initial=1000,
            step=1,
            handleRadius=5,
            vertical=True,
            handleColour=(g.r, g.g, g.b),
        )

        self.log_lines = []

        # self.log_scroll_tooltip = TextBox(
        #     self.screen, 455, 160, 40, 24, font=self.simple_font, fontSize=12
        # )
        # self.log_scroll_tooltip.disable()

    def create_hex_dump(self) -> None:
        """
        Draws the hex dump.
        """
        self.hex_lines.clear()
        viewable_ram = {}
        for key, value in self.hex_dump.items():
            proper_value = -self.hex_slider.getValue()
            if key <= 0x00F0 or (
                key >= proper_value and key < proper_value + (16 * 16)
            ):
                # print(hex(int(self.slider.getValue())), hex(key), value)
                viewable_ram[key] = value
        for key, value in viewable_ram.items():
            vals = " ".join([f"{val:02X}" for val in value])
            text = self.simple_font.render(
                f"0x{key:04X}: {vals}", True, pygame.Color("green1")
            )
            self.hex_lines[key] = text

    def create_log_lines(self):
        self.log_lines.clear()

        log_data = {}
        with open("nes.log", "r", encoding="utf-8") as file_:
            lines = file_.readlines()
            for i, line in enumerate(lines):
                text = self.simple_small_font.render(line.rstrip(), True, pygame.Color("green1"))
                log_data[i] = text
                self.log_lines.append(text)

    def blit_hexdump(self) -> None:
        """
        Blits the hex dump to the screen.
        """
        add_extra = 0
        self.screen: pygame.Surface
        inital_space = 24
        for i, (_, text) in enumerate(self.hex_lines.items()):
            if i % 8 == 0 and i != 0:
                # Add extra spacing for every 8 lines
                add_extra = (i / 8) * 16

            next_line_pos = (
                self.hex_dump_line_spacing + (inital_space + ((i - 1) * 16)) + add_extra
            )
            self.hexdump_str_y_position.append(next_line_pos)
            self.screen.blit(text, [14, next_line_pos])

    def blit_logs(self) -> None:
        self.screen: pygame.Surface
        inital_space = 469
        log_slider_inverted_value = self.log_slider.max - self.log_slider.getValue()
        
        current_line = 1
        for i, line in enumerate(self.log_lines):
            if not (log_slider_inverted_value <= i < log_slider_inverted_value + 19):
                continue
            next_line_pos = self.hex_dump_line_spacing + (inital_space + ((current_line - 1) * 16))
            current_line += 1
            self.screen.blit(line, [14, next_line_pos])

    def draw_hex_dump_view(self):
        """
        Draws the hex dump view on the screen.

        This method is responsible for drawing the hex dump view 
        on the screen. It creates a rectangular shape, fills it 
        with white color, and adds a title "Hex Dump" at the top 
        left corner. It also sets the scroll tooltip text based 
        on the slider value.

        """
        # rect = pygame.Rect(75 + (24 * 0), self.hexdump_str_y_position[1], 22, 17)
        # shape_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        # pygame.draw.rect(
        #     shape_surf, pygame.Color("yellow"), shape_surf.get_rect(), width=1
        # )
        # self.screen.blit(shape_surf, rect)

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
        self.hex_scroll_tooltip.setText(f"{-int(self.hex_slider.getValue()):04X}")

    def draw_log_box(self):
        """
        Draws the log box on the screen.

        This method is responsible for drawing the log box on the screen.
        It creates a rectangular shape, fills it with white color, and adds
        a title "Log" at the top left corner.

        """
        rect = pygame.Rect(0, 462, 800, 338)
        shape_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            shape_surf, pygame.Color("white"), shape_surf.get_rect(), width=3
        )

        text = self.bold_font.render(
            " Log Output" + str(" " * 89), True, pygame.Color("black")
        )
        temp_surface = pygame.Surface(text.get_size())
        temp_surface.fill(pygame.Color("white"))
        temp_surface.blit(text, (0, 0))
        self.screen.blit(temp_surface, [3, 465])

        self.screen.blit(shape_surf, rect)

    def check_128_byte_chunk(self, chunk) -> bool:
        """
        Checks if the current chunk of data is 128 bytes.

        Returns:
            bool: True if the current chunk of data is 128 bytes, False otherwise.
        """
        assert len(chunk) == 128
        return all(chunk == 0 for chunk in chunk)

    def load_from_file(self, ram_offset_: int, file_path_: str) -> int:
        """
        Loads the hex dump from a file.

        Args:
            ram_offset_ (int): The offset in the emulator's memory where the hex dump
            should be loaded. file_path_ (str): The path to the file containing
            the hex dump.
        """
        nes = Bus()
        current_ram_offset = nes.load_to_ram(ram_offset_, file_path_)
        ram = nes.ram
        for offset in range(0, len(ram), 128):
            chunk = ram[offset : offset + 128]
            if not self.check_128_byte_chunk(chunk):
                sixteen_byte_chunks = HexdumpViewer.split_into_16_bytes(chunk)
                for byte_chunk in sixteen_byte_chunks:
                    self.hex_dump[offset] = byte_chunk
                    offset += 16
        self.create_hex_dump()
        return current_ram_offset

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
        self.create_hex_dump()

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
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.bg_color = 0, 0, 0
        self.font_size = 16
        self.test_val = 20
        self.line_spacing = 28
        self.r_is_pressed = False

        self.ram_offset = 0x8000
        binary_file_len = 0
        file_name = "./cc65-example/build/bin/ex1.bin"
        with open(file_name, "rb") as f:
            data = f.read()
            binary_file_len = len(list(data))
        self.hex_dumper = HexdumpViewer(self.screen, self.ram_offset, binary_file_len)
        # self.hex_dumper.create()
        # asm_string = """
        # A2 0A 8E 00 00 A2 03 8E
        # 01 00 AC 00 00 A9 00 18
        # 6D 01 00 88 D0 FA 8D 02
        # 00 EA EA EA
        # """
        m = self.hex_dumper.load_from_file(self.ram_offset, file_name)
        self.hex_dumper.hex_slider.max = -self.ram_offset
        self.hex_dumper.hex_slider.min = -m
        self.hex_dumper.hex_slider.setValue(-self.ram_offset)

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
                self.hex_dumper.create_log_lines()
                self.draw()
                pygame_widgets.update(event)
                pygame.display.update()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    self.test_val += 1
                    print("test_val: ", self.test_val)
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    self.test_val -= 1
                    print("test_val: ", self.test_val)
                elif event.key == pygame.K_r:
                    print("r presed")
                elif event.key == pygame.K_DOWN:
                    v = self.hex_dumper.hex_slider.getValue()
                    if v > self.hex_dumper.hex_slider.min:
                        self.hex_dumper.hex_slider.setValue(v - 0x80)
                    self.hex_dumper.create_hex_dump()
                elif event.key == pygame.K_UP:
                    v = self.hex_dumper.hex_slider.getValue()
                    if v < self.hex_dumper.hex_slider.max:
                        self.hex_dumper.hex_slider.setValue(v + 0x80)
                    self.hex_dumper.create_hex_dump()
                elif event.key == pygame.K_q:
                    pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.hex_dumper.create_hex_dump()
                self.hex_dumper.create_log_lines()
                print("mouse up location: ", pygame.mouse.get_pos())

    def draw(self):
        """
        Draws the screen of the NES simulator.
        """
        self.screen.fill(self.bg_color)
        self.hex_dumper.blit_hexdump()
        self.hex_dumper.blit_logs()
        self.hex_dumper.draw_hex_dump_view()
        self.hex_dumper.draw_log_box()
        pygame.display.flip()


if __name__ == "__main__":
    with open("nes.log", 'w', encoding='utf-8') as file:
        pass
    # x = HexdumpViewer(None)
    # x.load_from_file(0x0080, "6502-mult.bin")
    NesSimulator().run()
    pygame.quit()
