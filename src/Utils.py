from Board import Board

__CONSOLE_COLOR_PALETTE = ['#', 'O', '=', '+', '@']

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
