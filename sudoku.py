import numpy as np
import IPython
from tkinter import *
fields = 'Last Name', 'First Name', 'Job', 'Country'


def fetch(board, values):
    row_ = 0
    for board_row in board:
        col_ = 0
        for entry in board_row:
            if entry.get():
                values[row_, col_] = entry.get()
            col_ += 1
        row_ += 1
    print(values)


def make_board(window):

    board = []
    for row_ in range(9):
        pady_ = (0, 0)
        board_row = []
        if row_ % 3 == 0:
            pady_ = (10, 0)
        for col_ in range(9):
            padx_ = (0, 0)
            if col_ % 3 == 0:
                padx_ = (10, 0)
            ent = Entry(width=2)
            ent.grid(row=row_, column=col_, padx=padx_, pady=pady_)
            board_row.append(ent)
        board.append(board_row)
    return board


def solve_soduku(values):
    iteration = 0
    while not np.all(values != 0):
        (values, changed_by_cross) = solve_by_cross(values)
        (values, changed_by_pencil) = solve_by_pencil(values)
        iteration += 1
        if not (changed_by_cross or changed_by_pencil):
            break

    if not np.all(values != 0):
        print('solver failed to finish solution')

    print('outer loop iteration = %d' % (iteration))
    return values


def solve_by_pencil(values):
    changed_at_all = False
    changed = True
    iteration = 0
    while changed:
        changed = False
        for row_ in range(9):
            for col_ in range(9):
                if values[row_, col_] == 0:
                    possible_numbers = get_possible_numbers(values, row_, col_)
                    if len(possible_numbers) == 1:
                        values[row_, col_] = possible_numbers[0]
                        changed = True
                        changed_at_all = True
        iteration += 1

    print(values)
    print('entry solver iteration = %d' % (iteration))

    return (values, changed_at_all)


def solve_by_cross(values):
    changed_at_all = False
    iteration = 0
    for n in range(1, 10):
        changed = True
        while changed:
            for cell_row_ in range(3):
                for cell_col_ in range(3):
                    (cell, changed) = cross_cell(values, n, cell_row_,
                                                 cell_col_)
                    changed_at_all = changed_at_all or changed
                    set_cell(values, cell_row_, cell_col_, cell)
            iteration += 1

    print(values)
    print('cell solver iteration = %d' % (iteration))

    return (values, changed_at_all)


def set_cell(values, cell_row, cell_col, cell):
    values[cell_row * 3:cell_row * 3 + 3, cell_col * 3:cell_col * 3 + 3] = cell


def cross_cell(values, n, cell_row, cell_col):
    changed = False
    current_cell = get_cell(values, cell_row, cell_col)
    if n in remaining_numbers(current_cell):
        possible_pos = current_cell == 0
        for row_ in range(3):
            abs_row = 3 * cell_row + row_
            current_row = values[abs_row, :]
            if n in current_row:
                possible_pos[row_, :] = False

        for col_ in range(3):
            abs_col = 3 * cell_col + col_
            current_col = values[:, abs_col]
            if n in current_col:
                possible_pos[:, col_] = False

        if np.count_nonzero(possible_pos) == 1:
            print(current_cell)
            current_cell = current_cell + n * possible_pos
            changed = True
            print(current_cell)
        return (current_cell, changed)
    else:
        return (current_cell, changed)


def get_possible_numbers(values, row, col):
    cell_row = int(row / 3)
    cell_col = int(col / 3)

    current_cell = get_cell(values, cell_row, cell_col)
    current_row = values[row, :]
    current_col = values[:, col]

    cell_remaining = remaining_numbers(current_cell)
    row_remaining = remaining_numbers(current_row)
    col_remaining = remaining_numbers(current_col)

    possible_numbers = cell_remaining.intersection(
        row_remaining.intersection(col_remaining))

    print('[%d][%d]: ' % (row, col), possible_numbers)
    return list(possible_numbers)


def get_cell(values, cell_row, cell_col):
    return values[cell_row * 3:cell_row * 3 + 3, cell_col * 3:cell_col * 3 + 3]


def remaining_numbers(array):
    sudoku_set = set(range(1, 10))
    existing_set = set(array[np.nonzero(array)])
    remaining_set = sudoku_set - existing_set

    return remaining_set


if __name__ == '__main__':
    values = np.zeros((9, 9))
    window = Tk()
    board = make_board(window)
    window.bind('<Return>', (lambda event, e=board: fetch(e, values)))
    b1 = Button(
        window, text='Submit', command=(lambda e=board: fetch(e, values)))
    b1.grid(row=9, column=9, padx=10, pady=10)
    b2 = Button(window, text='Finish', command=window.quit)
    b2.grid(row=9, column=10, padx=10, pady=10)
    window.mainloop()

    # values = np.array([[0., 6., 0., 0., 8., 0., 4., 2.,
    #                     0.], [0., 1., 5., 0., 6., 0., 3., 7.,
    #                           8.], [0., 0., 0., 4., 0., 0., 0., 6.,
    #                                 0.], [1., 0., 0., 6., 0., 4., 8., 3., 0.],
    #                    [3., 0., 6., 0., 1., 0., 7., 0.,
    #                     5.], [0., 8., 0., 3., 5., 0., 0., 0.,
    #                           0.], [8., 3., 0., 9., 4., 0., 0., 0., 0.],
    #                    [0., 7., 2., 1., 3., 0., 9., 0.,
    #                     0.], [0., 0., 9., 0., 2., 0., 6., 1., 0.]])
    #
    # values = np.array(values)

    solve_soduku(values)
    IPython.embed()
