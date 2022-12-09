import time
import pygame
import sys
from solver import solve, is_valid_move
from generator import generate_board

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
LINE_WIDTH = 2
MENU = "1. Click on the square you want to choose\n2. Enter a number (invalid input or 0 won't appear " \
       "on screen) \n3. While a number is red your choice is not final \n4. To finalize your choice, " \
       "click on the square you want to finalize and the press enter \n5. If you were correct the number " \
       "will turn black, else it will disappear and you'll get a strike \n6. Game is over when you'll get " \
       "3 strikes or when solving the sudoku \n7. To solve at any given moment, press s \n8.To quit press q"


# Render each word and check how many words can fit the screen
def blit_text(surface, text, pos, font, color=BLACK):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60
    clock = " " + str(minute) + ":" + str(sec) if hour == 0 else " " + str(hour) + ":" + str(minute) + ":" + str(sec)
    return clock


class Board:

    def __init__(self, board_game, board_width, menu_width):
        self.board_width = board_width
        self.menu_width = menu_width
        self.board_game = board_game
        self.selected = [-1, -1]  # selected by mouse click
        self.strikes = 0
        self.empty_cells = 0  # empty_cells == 0 iff sudoku is solved
        self.cells = []
        self.cell_width = board_width // 9
        for i in range(9):
            list_i = []
            for j in range(9):
                val = board_game[i][j]
                cell = Cell(val, val != 0, i, j, self.cell_width)
                list_i.append(cell)

                if board_game[i][j] == 0:
                    self.empty_cells += 1

            self.cells.append(list_i)

    def draw_menu(self, screen, font, play_time):
        space = 5
        pygame.draw.rect(screen, BLACK, (self.board_width - space, 0, self.menu_width + space, self.board_width), LINE_WIDTH)

        blit_text(screen, "MENU", (self.board_width + (self.menu_width // 3), 0), font, BLACK)
        font_size = 30
        font = pygame.font.SysFont("Ariel", font_size)
        blit_text(screen, MENU, (self.board_width + space, 75), font, BLACK)

        # time text
        some_text = font.render("Time: " + format_time(play_time), True, BLACK)
        screen.blit(some_text, (self.board_width - space, 2 * (self.board_width - font_size) // 3))

        # draw line -> (,)  -> (,) : from : to
        pygame.draw.line(screen, BLACK, (self.board_width - space, (2 * self.board_width // 3) - 3),
                                        (self.board_width + self.menu_width, (2 * self.board_width // 3) - 3), 3)

        # strikes text
        font_size = 80
        font = pygame.font.SysFont("Ariel", font_size)
        some_text = font.render("STRIKES", True, BLACK)
        screen.blit(some_text, (self.board_width + (self.board_width // 7), (2 * self.board_width // 3) + space * 3))

        # draw line -> (,)  -> (,) : from : to
        pygame.draw.line(screen, BLACK, (self.board_width - space, (2 * self.board_width // 3) + self.cell_width - 3),
                         (self.board_width + self.menu_width, (2 * self.board_width // 3) + self.cell_width - 3), 3)

        # draw strikes
        font_size = 120
        strike_space = 150
        font = pygame.font.SysFont("Ariel", font_size)
        for i in range(self.strikes):
            some_text = font.render("X", True, RED)
            screen.blit(some_text, ((self.board_width + (self.board_width // 11)) + i * strike_space, self.board_width - 1.5 * self.cell_width))

    def draw(self, screen, font, play_time):
        screen.fill(WHITE)

        # draw nodes
        for row in self.cells:
            for cell in row:
                cell.draw(screen, font)

        # draw menu
        self.draw_menu(screen, font, play_time)
        pygame.display.update()

    def get_clicked_pos(self, pos):
        x, y = pos
        row = x // self.cell_width
        col = y // self.cell_width

        return row, col

    def get_cell(self, row, col):
        if 0 <= row < 9 and 0 <= col < 9:
            # for the first click
            if self.selected[0] >= 0:
                self.cells[self.selected[0]][self.selected[1]].un_click()

            self.selected[0] = row
            self.selected[1] = col
            return self.cells[row][col]

        return None

    def strike(self):
        self.strikes += 1


class Cell:

    def __init__(self, val, immutable, row, col, width):
        self.val = val
        # cell.immutable == true iff cell.val is equal to cell.val in the solved board
        self.immutable = immutable
        self.selected = False
        self.row = row
        self.col = col
        self.width = width
        self.x = row * width
        self.y = col * width
        self.color = BLACK

    def draw(self, screen, font):
        offset = self.width // 3
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width), LINE_WIDTH)
        if self.immutable:
            val_text = font.render(str(self.val), True, BLACK)
        else:
            val_text = font.render(str(self.val), True, GRAY)
        if self.val != 0:
            screen.blit(val_text, pygame.Vector2(self.x + offset, self.y + offset // 2))

    def make_immutable(self):
        self.immutable = True

    def click(self):
        self.color = RED

    def un_click(self):
        self.color = BLACK

    def set_val(self, new_val):
        if not self.immutable:
            self.val = new_val
