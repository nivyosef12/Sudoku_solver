import copy
import time
import pygame as pg
import sys
from main import get_grid, solve, is_valid_move

pg.init()
screen_size = 1200, 750
offset = 15
board_size = 720
cell_size = 80
menu_explanation = "1. Click on the square you want to choose it \n2. Enter a number (invalid input or 0 won't appear " \
                   "on the board \n3. While a number is red your choice is not final \n4. To finalize your choice, " \
                   "click on the square you want to finalize and the press enter \n5. If you were correct the number " \
                   "will turn black, else it will disappear and you'll get a strike \n6. Game is over when you'll get " \
                   "3 strikes or when solving the sudoku \n7. To solve at any given moment, press s "


class Board:

    def __init__(self, board_game):
        self.board_game = board_game
        self.selected = (-1, -1)  # selected by mouse click
        self.strikes = 0
        self.cells = []
        self.empty_cells = 0
        for i in range(9):
            list_i = []
            for j in range(9):
                val = board_game[i][j]
                list_i.append(Cell(val, val != 0))
                if board_game[i][j] == 0:
                    self.empty_cells += 1
            self.cells.append(list_i)


class Cell:

    def __init__(self, val, immutable):
        self.val = val
        self.immutable = immutable


def draw_background(screen, board, play_time):
    screen.fill(pg.Color("white"))
    # draw game board
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(offset, offset, board_size, board_size), 10)
    i = 1
    while i * cell_size < board_size:
        line_width = 5 if i % 3 > 0 else 10
        # drew vertical lines
        pg.draw.line(screen, pg.Color("black"), ((i * cell_size) + offset, offset),
                     ((i * cell_size) + offset, (board_size + offset)), line_width)
        # drew horizontal lines
        pg.draw.line(screen, pg.Color("black"), (offset, (i * cell_size) + offset),
                     ((board_size + offset), (i * cell_size) + offset), line_width)
        draw_menu(screen, board, line_width, i, play_time)
        i += 1
        # paint clicked cell with red
        if board.selected != (-1, -1) and not board.cells[board.selected[0]][board.selected[1]].immutable:
            selected_rect = pg.Rect(offset + (cell_size * board.selected[1]),
                                    offset + (cell_size * board.selected[0]), cell_size, cell_size)
            pg.draw.rect(screen, pg.Color("red"), selected_rect, 10)


def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60
    clock = " " + str(minute) + ":" + str(sec) if hour == 0 else " " + str(hour) + ":" + str(minute) + ":" + str(sec)
    return clock


# Render each word and check how many words can fit the screen
def blit_text(surface, text, pos, font, color=pg.Color('black')):
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


def draw_menu(screen, board, line_width, i, play_time):
    font = pg.font.SysFont("Segoe UI", 20)
    blit_text(screen, menu_explanation, (screen_size[1], offset * 2 + 10), font, pg.Color('black'))
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(board_size + offset, offset, 465, board_size), 10)
    time_text = font.render("Time: " + format_time(play_time), True, pg.Color("black"))
    screen.blit(time_text, (screen_size[1], 460))
    if i == 6 or i == 7:
        pg.draw.line(screen, pg.Color("black"), ((offset + board_size), offset + (i * cell_size)),
                     (screen_size[0], offset + (i * cell_size))
                     , line_width)
        if i == 6:
            font = pg.font.SysFont("Ariel", cell_size)
            strikes_text = font.render('STRIKES', True, pg.Color("black"))
            screen.blit(strikes_text, ((500 + screen_size[0]) // 2, (((i * cell_size) + ((i + 1) * cell_size)) // 2) - 5))
        else:  # draw strikes
            for j in range(board.strikes):
                font = pg.font.SysFont(None, 120)
                strikes_text = font.render('X', True, pg.Color("red"))
                screen.blit(strikes_text,
                            (((450 + screen_size[0]) // 2) + j * 120, (((i * cell_size) + ((i + 2) * cell_size)) // 2) - 20))


def draw_numbers(screen, font, board):
    row = 0
    offset_ = 35
    # board_game = board.board_game
    while row < 9:
        col = 0
        while col < 9:
            num = board.cells[row][col].val
            if num != 0:
                if board.cells[row][col].immutable:
                    n_text = font.render(str(num), True, pg.Color("black"))
                else:
                    n_text = font.render(str(num), True, pg.Color("red"))
                screen.blit(n_text, pg.Vector2((col * cell_size) + offset + 25, (row * cell_size) + offset + 18))
            col += 1
        row += 1


def draw(screen, font, board, play_time):
    draw_background(screen, board, play_time)
    draw_numbers(screen, font, board)
    pg.display.flip()


def make_change(board, key):
    selected = board.selected
    cell_to_be_changed = board.cells[selected[0]][selected[1]]
    if not cell_to_be_changed.immutable:
        board_game = board.board_game
        if is_valid_move(board_game, key, selected):
            cell_to_be_changed.val = key
            board_game[selected[0]][selected[1]] = key
        else:
            cell_to_be_changed.val = 0
            board_game[selected[0]][selected[1]] = 0


def check_move(board):
    cell = board.cells[board.selected[0]][board.selected[1]]
    if cell.val == 0:
        return True
    if cell.val != 0 and not cell.immutable:
        if solve(copy.deepcopy(board.board_game)):
            cell.immutable = True
            board.empty_cells -= 1
        else:
            cell.val = 0
            board.board_game[board.selected[0]][board.selected[1]] = 0
    return cell.immutable


def main():
    board = Board(get_grid(1))  # deep copy??
    screen = pg.display.set_mode(screen_size)
    font = pg.font.SysFont(None, 80)
    pg.display.set_caption("Sudoku")
    board_game = board.board_game
    start = time.time()
    while 1:
        play_time = round(time.time() - start)
        key = None
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                if pos[0] < offset or pos[0] > (offset + board_size) or pos[1] < offset or pos[1] > (offset + board_size):
                    board.selected = (-1, -1)
                else:
                    board.selected = (((pos[1] - 15) // cell_size), ((pos[0] - 15) // cell_size))
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    if not solve(board_game):
                        print("no possible solution for that current board")
                        sys.exit()
                    for i in range(len(board_game)):
                        for j in range(len(board_game)):
                            board.cells[i][j].val = board_game[i][j]
                if event.key == pg.K_KP_ENTER and board.selected != (-1, -1):
                    print(board.empty_cells)
                    if not check_move(board):
                        board.strikes += 1
                if event.key == pg.K_0 and board.selected != (-1, -1):
                    key = 0
                if event.key == pg.K_1 and board.selected != (-1, -1):
                    key = 1
                if event.key == pg.K_2 and board.selected != (-1, -1):
                    key = 2
                if event.key == pg.K_3 and board.selected != (-1, -1):
                    key = 3
                if event.key == pg.K_4 and board.selected != (-1, -1):
                    key = 4
                if event.key == pg.K_5 and board.selected != (-1, -1):
                    key = 5
                if event.key == pg.K_6 and board.selected != (-1, -1):
                    key = 6
                if event.key == pg.K_7 and board.selected != (-1, -1):
                    key = 7
                if event.key == pg.K_8 and board.selected != (-1, -1):
                    key = 8
                if event.key == pg.K_9 and board.selected != (-1, -1):
                    key = 9
        if key is not None:
            make_change(board, key)
        draw(screen, font, board, play_time)
        if board.strikes >= 3:
            print("game over")
            break
        if board.empty_cells == 0:
            print("finished")
            break


main()
