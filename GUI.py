import pygame as pg
import sys
from main import get_grid, solve, is_valid_move

pg.init()
screen_size = 750, 750


def draw_background(screen):
    screen.fill(pg.Color("white"))
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(15, 15, 720, 720), 10)
    i = 1
    while i * 80 < 720:
        line_width = 5 if i % 3 > 0 else 10
        # drew vertical lines
        pg.draw.line(screen, pg.Color("black"), pg.Vector2((i * 80) + 15, 15), pg.Vector2((i * 80) + 15, 735)
                     , line_width)
        # drew horizontal lines
        pg.draw.line(screen, pg.Color("black"), pg.Vector2(15, (i * 80) + 15), pg.Vector2(735, (i * 80) + 15)
                     , line_width)
        i += 1


def draw_numbers(screen, font, board):
    row = 0
    offset = 35
    while row < 9:
        col = 0
        while col < 9:
            num = board[row][col]
            if num != 0:
                n_text = font.render(str(num), True, pg.Color("black"))
                screen.blit(n_text, pg.Vector2((col * 80) + offset + 5, (row * 80) + offset - 2))
            col += 1
        row += 1


def draw(screen, font, grid):
    draw_background(screen)
    draw_numbers(screen, font, grid)
    pg.display.flip()


def main():
    screen = pg.display.set_mode(screen_size)
    font = pg.font.SysFont(None, 80)
    pg.display.set_caption("Sudoku")
    grid = get_grid()
    key = None
    while 1:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    solve(grid)
                if event.key == pg.K_1:
                    key = 1
                if event.key == pg.K_2:
                    key = 2
                if event.key == pg.K_3:
                    key = 3
                if event.key == pg.K_4:
                    key = 4
                if event.key == pg.K_5:
                    key = 5
                if event.key == pg.K_6:
                    key = 6
                if event.key == pg.K_7:
                    key = 7
                if event.key == pg.K_8:
                    key = 8
                if event.key == pg.K_9:
                    key = 9
        draw(screen, font, grid)


main()
