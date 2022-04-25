import pygame as pg
import sys
from main import get_grid, solve, is_valid_move

pg.init()
screen_size = 750, 750


class Board:

    def __init__(self, board_game):
        self.board_game = board_game
        self.selected = (-1, -1)  # selected by mouse click
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
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(offset, offset, 720, 720), 10)
    i = 1
    while i * 80 < 720:
        line_width = 5 if i % 3 > 0 else 10
        # drew vertical lines
        pg.draw.line(screen, pg.Color("black"), pg.Vector2((i * 80) + offset, offset), pg.Vector2((i * 80) + offset, 735)
                     , line_width)
        # drew horizontal lines
        pg.draw.line(screen, pg.Color("black"), pg.Vector2(offset, (i * 80) + offset), pg.Vector2(735, (i * 80) + offset)
                     , line_width)
        i += 1
        # paint clicked cell with red
        if board.selected != (-1, -1) and not board.cells[board.selected[0]][board.selected[1]].immutable:
            selected_rect = pg.Rect(offset + (80 * board.selected[1]), offset + (80 * board.selected[0]), 80, 80)
            pg.draw.rect(screen, pg.Color("red"), selected_rect, 10)


def draw_numbers(screen, font, board):
    row = 0
    offset = 35
    board_game = board.board_game
    while row < 9:
        col = 0
        while col < 9:
            num = board_game[row][col]
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
    if not board.cells[selected[0]][selected[1]].immutable:
        board_game = board.board_game
        if is_valid_move(board_game, key, selected):
            board_game[selected[0]][selected[1]] = key
        else:
            board_game[selected[0]][selected[1]] = 0


def main():
    screen = pg.display.set_mode(screen_size)
    font = pg.font.SysFont(None, 80)
    pg.display.set_caption("Sudoku")
    board = Board(get_grid())
    board_game = board.board_game
    strikes = 0
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
                    print(board.selected)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    if not solve(board_game):
                        print("no possible solution for that current board")
                        sys.exit()
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


main()
