import random
from solver import solve, find_empty, is_valid_move


# board is 9X9
# returns true iff num of solutions of board is 1
def is_unique_solution(board, num_of_solutions):
    if num_of_solutions < 2:
        find = find_empty(board)
        if not find: # board is full
            return True
        row, col = find
        for num in range(1, 10):
            if num_of_solutions < 2 and is_valid_move(board, num, (row, col)):
                board[row][col] = num
                if is_unique_solution(board, num_of_solutions):
                    num_of_solutions += 1
                board[row][col] = 0
        return num_of_solutions == 1
    return False


def generate_board():
    board = [[0 for i in range(1, 10)] for j in range(1, 10)]
    solve(board)
    cells = [(j, i) for i in range(0, 9) for j in range(0, 9)]
    random.shuffle(cells)
    i = 0
    for cell in cells:
        if i < 50:  # TODO difficulty
            temp = board[cell[0]][cell[1]]
            board[cell[0]][cell[1]] = 0
            if not is_unique_solution(board.copy(), 0):
                board[cell[0]][cell[1]] = temp
            i += 1
    return board
