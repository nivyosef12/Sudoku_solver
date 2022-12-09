import random
from solver import solve, find_empty, is_valid_move

HARD = 60
MEDIUM = 50
EASY = 40


# board is 9X9
# returns true iff num of solutions of board is 1
def is_unique_solution(board, num_of_solutions):
    if num_of_solutions < 2:

        # find next empty cell
        find = find_empty(board)

        if not find:  # board is full
            return True

        row, col = find
        for num in range(1, 10):

            if num_of_solutions < 2 and is_valid_move(board, num, (row, col)):

                # try num at board[row][col]
                board[row][col] = num

                if is_unique_solution(board, num_of_solutions):
                    num_of_solutions += 1

                # try board[row][col] with another num (num + 1 for num in range (1, 9)) to see if there is
                # another possible solution
                board[row][col] = 0

        return num_of_solutions == 1

    return False


def generate_board():
    # generate 9X9 board
    board = [[0 for i in range(1, 10)] for j in range(1, 10)]

    # solve empty board to generate a (full) valid sudoku board
    solve(board)

    # get the cells of board in random order
    cells = [(j, i) for i in range(0, 9) for j in range(0, 9)]
    random.shuffle(cells)

    difficulty = 0
    for cell in cells:
        if difficulty < MEDIUM:
            # hide real val of cell
            temp = board[cell[0]][cell[1]]
            board[cell[0]][cell[1]] = 0

            # check if solution is still unique
            if not is_unique_solution(board.copy(), 0):
                board[cell[0]][cell[1]] = temp

            difficulty += 1

    return board
