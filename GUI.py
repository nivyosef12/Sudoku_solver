import pygame as pg
import sys
# import get grid from main -> what is the problem

pg.init()
screen_size = 750, 750
screen = pg.display.set_mode(screen_size)
font = pg.font.SysFont(None, 80)


def get_grid():
    option = int(input("Would you like to generate a board (1) or to play with specefic board? (2)\n"))
    if option == 1:
        return [  # generate
            [7, 8, 0, 4, 0, 0, 1, 2, 0],
            [6, 0, 0, 0, 7, 5, 0, 0, 9],
            [0, 0, 0, 6, 0, 1, 0, 7, 8],
            [0, 0, 7, 0, 4, 0, 2, 6, 0],
            [0, 0, 1, 0, 5, 0, 9, 3, 0],
            [9, 0, 4, 0, 6, 0, 0, 0, 5],
            [0, 7, 0, 3, 0, 0, 0, 1, 2],
            [1, 2, 0, 0, 0, 7, 4, 0, 0],
            [0, 4, 9, 2, 0, 6, 0, 0, 7]
        ]
    grid = []
    for i in range(1, 10):
        row = list(input("Enter Row " + str(i) + " nums: \n"))
        while len(row) != 9:
            row = list(input("Invalid number of elements, please enter again: \n"))
        lst = []
        for n in row:
            lst.append(int(n))
        grid.append(lst)
    return grid


def draw_background():
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


def draw_numbers(board):
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


def main():
    # in commit -> grid creation takes place at main func, get grid added
    grid = get_grid()
    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
        draw_background()
        draw_numbers(grid)
        pg.display.flip()


main()
