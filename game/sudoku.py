import random
import copy

SIZE = 9

# -----------------------------
# Find empty cell
# -----------------------------
def find_empty(board):
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == 0:
                return i, j
    return None


# -----------------------------
# Check valid number
# -----------------------------
def is_valid(board, row, col, num):
    # row
    if num in board[row]:
        return False

    # column
    for i in range(9):
        if board[i][col] == num:
            return False

    # 3x3 box
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3

    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num:
                return False

    return True


# -----------------------------
# Solve board (backtracking)
# -----------------------------
def solve_board(board):
    find = find_empty(board)
    if not find:
        return True

    row, col = find

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_board(board):
                return True
            board[row][col] = 0

    return False


# -----------------------------
# Fill board randomly (THIS WAS MISSING)
# -----------------------------
def fill_board(board):
    find = find_empty(board)
    if not find:
        return True

    row, col = find
    numbers = list(range(1, 10))
    random.shuffle(numbers)

    for num in numbers:
        if is_valid(board, row, col, num):
            board[row][col] = num
            if fill_board(board):
                return True
            board[row][col] = 0

    return False


# -----------------------------
# Remove cells based on level
# -----------------------------
def remove_cells(board, level):
    if level == "easy":
        remove = 35
    elif level == "medium":
        remove = 45
    else:
        remove = 55

    while remove > 0:
        r = random.randint(0, 8)
        c = random.randint(0, 8)

        if board[r][c] != 0:
            board[r][c] = 0
            remove -= 1

    return board


# -----------------------------
# Generate Sudoku
# -----------------------------
def generate_sudoku(level="easy"):
    board = [[0 for _ in range(9)] for _ in range(9)]

    fill_board(board)

    solution = copy.deepcopy(board)
    puzzle = remove_cells(board, level)

    return puzzle, solution
