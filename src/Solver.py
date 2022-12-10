import numpy as np
import itertools as it
import pycosat as sat
from Board import Board
from Utils import copy_2d_list

# TODO: Redefine the old things
# T : The big table HMMM
# x : a propositional variables array from 0 to n + 1

def solve(board : Board):
    """ Returns a new solved board """
    cnf, indices = _get_cnf(board)
    sol = list(sat.solve(cnf)) # We suppose there is only one solution
    assert sol != "UNSAT", "This nonogram has no solution"
    solved = Board(board.size, copy_2d_list(board.constraints))
    grid = []
    for i in indices:
        grid += sol[i[0]:i[1]]
    solved.grid = np.array(grid)[:].reshape(board.size[0], board.size[1]) > 0
    return solved

def _get_cnf(board : Board):
    n, m = board.size
    cnf = []
    counter = 1
    cstr_counter = 0
    indices = []
    for _ in range(n):
        xsize = m + 2
        ssize = (m + 1) ** 2
        x = np.arange(counter, counter + xsize)
        s = np.arange(counter + xsize, counter + xsize + ssize).reshape((m + 1, m + 1))
        constraints = board.constraints[cstr_counter]

        indices.append((counter, counter + m))

        cstr_counter += 1
        counter += xsize + ssize

        cnf += _np_cnf_to_int(_C(x, s, m) + _B(x, s, constraints, m))
        
    for i in range(m):
        xsize = n + 2
        ssize = (n + 1) ** 2
        x = np.arange(counter, counter + xsize)
        s = np.arange(counter + xsize, counter + xsize + ssize).reshape((n + 1, n + 1))
        constraints = board.constraints[cstr_counter]
        
        counter += xsize + ssize
        cstr_counter += 1

        cnf += _np_cnf_to_int(_C(x, s, n) + _B(x, s, constraints, n))

    return cnf, indices



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