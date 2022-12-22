# TODO list
# 1. add choose difficulty option
# 2. add game over menu

import pygame
import time
from gameBoard import Board
from solver import solve, print_board
from generator import generate_board

pygame.init()
pygame.display.set_caption("Sudoku")

MENU_WIDTH = 500
BOARD_WIDTH = 750
SCREEN = pygame.display.set_mode((BOARD_WIDTH + MENU_WIDTH, BOARD_WIDTH))
FONT = pygame.font.SysFont("Ariel", 80)


def main():
    solved_board = generate_board()
    print_board(solved_board)
    print("\n--------------------------\n")
    game_board = Board(solved_board, BOARD_WIDTH, MENU_WIDTH)
    # will be used to check if a players move is legal since there's only one possible solution
    if not solve(solved_board):
        print("possible? CHECK!")
        # try again
    print_board(solved_board)

    run = True
    game_over = False
    curr_cell = None
    start_time = time.time()

    while run:
        play_time = round(time.time() - start_time)
        game_board.draw(SCREEN, FONT, play_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # left click
                # get clicked cell
                pos = pygame.mouse.get_pos()
                row, col = game_board.get_clicked_pos(pos)

                curr_cell = game_board.get_cell(row, col)
                if curr_cell is not None:
                    curr_cell.click()

            if event.type == pygame.KEYDOWN:

                # quit
                if event.key == pygame.K_q:
                    run = False

                # solve
                if event.key == pygame.K_s:
                    for i in range(0, 9):
                        for j in range(0, 9):
                            game_board.get_cell(i, j).set_val(solved_board[i][j])
                    game_over = True

                # check if move is legal
                if event.key == pygame.K_KP_ENTER and curr_cell is not None:
                    if curr_cell.val != solved_board[curr_cell.row][curr_cell.col]:
                        game_board.strike()
                    else:
                        curr_cell.make_immutable()

                # fill numbers
                if event.key == pygame.K_0 and curr_cell is not None:
                    curr_cell.set_val(0)

                if event.key == pygame.K_1 and curr_cell is not None:
                    curr_cell.set_val(1)

                if event.key == pygame.K_2 and curr_cell is not None:
                    curr_cell.set_val(2)

                if event.key == pygame.K_3 and curr_cell is not None:
                    curr_cell.set_val(3)

                if event.key == pygame.K_4 and curr_cell is not None:
                    curr_cell.set_val(4)

                if event.key == pygame.K_5 and curr_cell is not None:
                    curr_cell.set_val(5)

                if event.key == pygame.K_6 and curr_cell is not None:
                    curr_cell.set_val(6)

                if event.key == pygame.K_7 and curr_cell is not None:
                    curr_cell.set_val(7)

                if event.key == pygame.K_8 and curr_cell is not None:
                    curr_cell.set_val(8)

                if event.key == pygame.K_9 and curr_cell is not None:
                    curr_cell.set_val(9)

    pygame.quit()


if __name__ == '__main__':
    main()
