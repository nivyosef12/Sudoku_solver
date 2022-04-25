import copy

import pygame as pg
import sys
from main import get_grid, solve, is_valid_move

pg.init()
screen_size = 1200, 750
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
        for i in range(9):
            list_i = []
            for j in range(9):
                val = board_game[i][j]
                list_i.append(Cell(val, val != 0))
            self.cells.append(list_i)


class Cell:

    def __init__(self, val, immutable):
        self.val = val
        self.immutable = immutable


def draw_background(screen, board):
    screen.fill(pg.Color("white"))
    offset = 15
    # draw game board
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(offset, offset, 720, 720), 10)
    i = 1
    while i * 80 < 720:
        line_width = 5 if i % 3 > 0 else 10
        # drew vertical lines
        pg.draw.line(screen, pg.Color("black"), ((i * 80) + offset, offset), ((i * 80) + offset, 735)
                     , line_width)
        # drew horizontal lines
        pg.draw.line(screen, pg.Color("black"), (offset, (i * 80) + offset), (735, (i * 80) + offset)
                     , line_width)
        draw_menu(screen, board, line_width, i, offset)
        i += 1
        # paint clicked cell with red
        if board.selected != (-1, -1) and not board.cells[board.selected[0]][board.selected[1]].immutable:
            selected_rect = pg.Rect(offset + (80 * board.selected[1]), offset + (80 * board.selected[0]), 80, 80)
            pg.draw.rect(screen, pg.Color("red"), selected_rect, 10)
    # draw menu


def draw_menu(screen, board, line_width, i, offset):
    font = pg.font.SysFont("Segoe UI", 20)
    lines = menu_explanation.splitlines()
    for j, line in enumerate(lines):
        menu_text = font.render(line, True, pg.Color("black"))
        screen.blit(menu_text, (screen_size[1], offset * j * 2 + 30))
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(720 + offset, offset, 465, 720), 10)
    if i == 6 or i == 7:
        pg.draw.line(screen, pg.Color("black"), (735, offset + (i * 80)), (screen_size[0], offset + (i * 80))
                     , line_width)
        if i == 6:
            font = pg.font.SysFont("Ariel", 80)
            strikes_text = font.render('STRIKES', True, pg.Color("black"))
            screen.blit(strikes_text, ((500 + screen_size[0]) // 2, (((i * 80) + ((i + 1) * 80)) // 2) - 5))
        else:
            for j in range(board.strikes):
                font = pg.font.SysFont(None, 120)
                strikes_text = font.render('X', True, pg.Color("red"))
                screen.blit(strikes_text,
                            (((450 + screen_size[0]) // 2) + j * 120, (((i * 80) + ((i + 2) * 80)) // 2) - 20))


def draw_numbers(screen, font, board):
    row = 0
    offset = 35
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
                screen.blit(n_text, pg.Vector2((col * 80) + offset + 5, (row * 80) + offset - 2))
            col += 1
        row += 1


def draw(screen, font, board):
    draw_background(screen, board)
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
    while 1:
        key = None
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                if pos[0] < 15 or pos[0] > 735 or pos[1] < 15 or pos[1] > 735:
                    board.selected = (-1, -1)
                else:
                    board.selected = (((pos[1] - 15) // 80), ((pos[0] - 15) // 80))
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    if not solve(board_game):
                        print("no possible solution for that current board")
                        sys.exit()
                    for i in range(len(board_game)):
                        for j in range(len(board_game)):
                            board.cells[i][j].val = board_game[i][j]
                if event.key == pg.K_KP_ENTER and board.selected != (-1, -1):
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
        draw(screen, font, board)
        if board.strikes >= 3:
            print("game over")
            break


main()
