from Board import Board

__CONSOLE_COLOR_PALETTE = ['#', 'O', '=', '+', '@']
WHITE = 0
BLACK = 1
RED = 2
GREEN = 3
GRAY = 4
int_to_color = {
    0: 'white',
    1: 'black',
    2: 'red',
    3: 'green',
    4: 'gray'
}
color_to_int = {
    'white': 0,
    'black': 1,
    'red': 2,
    'green': 3,
    'gray': 4
}

def copy_2d_list(l):
    return [s[:] for s in l]

def display_console_board(board: Board):
    for l in board.grid:
        for c in l:
            if c == 0:
                print(' ', end=' ')
                continue
            print(__CONSOLE_COLOR_PALETTE[(c - 1) % len(__CONSOLE_COLOR_PALETTE)], end=' ')
        print()
