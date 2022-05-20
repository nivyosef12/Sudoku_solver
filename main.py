import random


# board is 9X9

def is_unique_solution(board, num_of_solutions):
    if num_of_solutions < 2:
        find = find_empty(board)
        if not find:
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
    solve(board, True)
    cells = [(j, i) for i in range(0, 9) for j in range(0, 9)]
    random.shuffle(cells)
    i = 0
    for cell in cells:
        if i < 30:  # TODO difficulty
            temp = board[cell[0]][cell[1]]
            board[cell[0]][cell[1]] = 0
            if not is_unique_solution(board.copy(), 0):
                board[cell[0]][cell[1]] = temp
            i += 1
    return board


def get_grid(option):
    if option == 1:
        return generate_board()
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


def solve(board, random_mode):
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find
    nums = [i for i in range(1, 10)]
    random.shuffle(nums)
    for num in nums:
        if is_valid_move(board, num, (row, col)):
            board[row][col] = num
            if solve(board, False):
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


def main():
    option = int(input("Would you like to generate a board (1) or to play with specefic board? (2)\n"))
    grid = get_grid(option)
    print_board(grid)
    if solve(grid, False):
        print("solved board is: ")
        print_board(grid)
    else:
        print("no possible solution")


if __name__ == '__main__':
    main()
