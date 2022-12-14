import numpy as np
import itertools as it
import pycosat as sat
from Board import Board
from Level import Level
from Utils import copy_2d_list

# TODO: Redefine the old things
# T : The big table HMMM
# x : a propositional variables array from 0 to n + 1

def solve(level: Level):
    """ Returns a new solved board """
    cnf = _get_cnf(level)
    #print(len(list(sat.itersolve(cnf))))
    sol = sat.solve(cnf) # We suppose there is only one solution
    assert sol != "UNSAT", "This nonogram has no solution"

    sol = list(sol)
    n, m = level.size
    grid = []
    for i in range(m):
        grid.append(sol[(n + 2) * (i + 1) + 1:(n + 2) * (i + 2) - 1])

    grid = np.array(grid)[:].reshape(level.size[0], level.size[1])
        

    solved = Board(level.size, False)
    solved.grid = np.where(grid > 0, 1, 0)

    return solved

def _get_cnf(level : Level):
    # Could've been made cleaner, way cleaner...
    n, m = level.size
    cnf = []

    x_grid = np.arange(1, (m + 2) * (n + 2) + 1).reshape((m + 2, n + 2))
    counter = (m + 2) * (n + 2)

    for i in range(m):
        x = x_grid[i + 1]
        s = np.arange(counter, counter + (n + 1)**2).reshape((n + 1, n + 1))
        row_constraint = level.constraints[i + n]

        counter += (n + 1)**2

        cnf += _np_cnf_to_int(_B(x, s, row_constraint, n) + _C(x, s, n))

    for j in range(n):
        x = x_grid[:, j + 1]
        s = np.arange(counter, counter + (m + 1)**2).reshape((m + 1, m + 1))
        counter += (m + 1)**2
        column_constraint = level.constraints[j]

        cnf += _np_cnf_to_int(_B(x, s, column_constraint, m) + _C(x, s, m))

    return cnf



def _Bb(x, s, i, n):
    return [[-s[i, j], -x[j], -x[j+1]] for j in range(n + 1)]

def _Ba(x, s, i, n):
    return [[-s[i, j], -x[j], x[j+1]] for j in range(n + 1)]

def _B(x, s, L, n):
    I = set()
    c = 0
    for y in L:
        c += y
        I.add(c)
    cnf = [[-x[0]], [-x[n + 1]], [s[sum(L), n]]]
    for i in range(n + 1):
        if i in I:
            cnf += _Bb(x, s, i, n)
        else:
            cnf += _Ba(x, s, i, n)
    return cnf

def _C10_bis(s, n):
    return [[-s[i, 1]] for i in range(2, n + 1)]

def _C11(s, n):
    cnf = []
    for j in range(n + 1):
        cnf += [[-s[i, j]] for i in range(j + 1, n + 1)]
    return cnf

def _C12(x, s, n):
    cnf = []
    for i in range(n + 1):
        cnf += [[-s[i, j], x[j + 1], s[i, j + 1]] for j in range(n)]
    return cnf

def _C13(x, s, n):
    cnf = []
    for i in range(n + 1):
        cnf += [[-s[i, j + 1], x[j + 1], s[i, j]] for j in range(n)]
    return cnf

def _C14(x, s, n):
    cnf = []
    for i in range(n):
        cnf += [[-s[i, j], -x[j + 1], s[i + 1, j + 1]] for j in range(n)]
    return cnf

def _C15(x, s, n):
    cnf = []
    for i in range(n):
        cnf += [[-s[i + 1, j + 1], -x[j + 1], s[i, j]] for j in range(n)]
    return cnf

def _C(x, s, n):
    return _C11(s, n) + _C12(x, s, n) + _C13(x, s, n) + _C14(x, s, n) + _C15(x, s, n) + [[s[0, 0]]]

def _np_cnf_to_int(cnf):
    return [[int(p) for p in d] for d in cnf]

def _show_sol(sol, simplified = False):
    if type(sol) == str:
        print(sol)
        return
    l = ['0' if i < 0 else '1' for i in sol]
    if simplified:
        print("sol :", " ".join(l[1:9]))
        return
    print("sol :", " ".join(l[:10]))
    l = np.array(l[10:]).reshape((n + 1, n + 1))
    for sub_l in l:
        print(" ".join(sub_l))

if __name__ == "__main__":
    L = (3, 2)
    n = 8
    x = np.arange(1, n + 3)
    s = np.arange(n + 3, n + 3 + (n + 1) ** 2).reshape((n + 1, n + 1))
    print(x)
    print(s)
    #s *= -1
    #np.fill_diagonal(s, 1)

    cnf = _C(x, s, n) + _B(x, s, L, n)
    cnf = _np_cnf_to_int(cnf)

    sols = sat.itersolve(cnf)
    for sol in sols:
        _show_sol(sol, True)
        #print(np.array(sol) > 0)
    #print(" ".join('0' if i < 0 else '1' for i in sol))