import random


def solve(board):
    find = find_empty(board)
    if not find:  # board if full
        return True
    else:
        row, col = find
    nums = [i for i in range(1, 10)]
    random.shuffle(nums)
    for num in nums:
        if is_valid_move(board, num, (row, col)):
            board[row][col] = num
            if solve(board):
                return True
            board[row][col] = 0
    return False


def is_valid_move(board, num, pos):
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:  # check row
            return False
        if board[i][pos[1]] == num and pos[0] != i:  # check column
            return False

    # check box
    box_x = pos[0] // 3
    box_y = pos[1] // 3
    for i in range(box_x * 3, box_x * 3 + 3):
        for j in range(box_y * 3, box_y * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    return True


def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:  # last position
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")


def find_empty(board):  # finds the next empty cell in the board
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return i, j  # row, col
    return None
