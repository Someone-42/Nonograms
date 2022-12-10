import numpy as np
import itertools as it
import pycosat as sat

# TODO: Redefine the old things
# T : The big table HMMM
# x : a propositional variables array from 0 to n + 1

n = 8
T = None

def get_cnf(T):
    pass

def _Bb(x, s, i):
    return [[-s[i, j], -x[j], -x[j+1]] for j in range(n + 1)]

def _Ba(x, s, i):
    return [[-s[i, j], -x[j], x[j+1]] for j in range(n + 1)]

def _B(x, s, L):
    I = set()
    c = 0
    for y in L:
        c += y
        I.add(c)
    cnf = [[-x[0]], [-x[n + 1]], [s[sum(L), n]]]
    for i in range(n + 1):
        if i in I:
            cnf += _Bb(x, s, i)
        else:
            cnf += _Ba(x, s, i)
    return cnf

def _C10(s):
    cnf = []
    for i in range(n + 1):
        cnf += [[-s[i, 1], s[0, 1], s[1, 1]], [-s[i, 1], -s[0, 1], -s[1, 1]]]
    return cnf

def _C10_bis(s):
    return [[-s[i, 1]] for i in range(2, n + 1)]

def _C11(s):
    cnf = []
    for j in range(n + 1):
        cnf += [[-s[i, j]] for i in range(j + 1, n + 1)]
    return cnf

def _C12(x, s):
    cnf = []
    for i in range(n + 1):
        cnf += [[-s[i, j], x[j + 1], s[i, j + 1]] for j in range(n)]
    return cnf

def _C13(x, s):
    cnf = []
    for i in range(n + 1):
        cnf += [[-s[i, j + 1], x[j + 1], s[i, j]] for j in range(n)]
    return cnf

def _C14(x, s):
    cnf = []
    for i in range(n):
        cnf += [[-s[i, j], -x[j + 1], s[i + 1, j + 1]] for j in range(n)]
    return cnf

def _C15(x, s):
    cnf = []
    for i in range(n):
        cnf += [[-s[i + 1, j + 1], -x[j + 1], s[i, j]] for j in range(n)]
    return cnf

def _C(x, s):
    return _C10_bis(s) + _C11(s) + _C12(x, s) + _C13(x, s) + _C14(x, s) + _C15(x, s) + [[s[0, 0]]]

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
    x = np.arange(1, n + 3)
    s = np.arange(n + 3, n + 3 + (n + 1) ** 2).reshape((n + 1, n + 1))
    print(x)
    print(s)
    #s *= -1
    #np.fill_diagonal(s, 1)

    cnf = _C(x, s) + _B(x, s, L)
    cnf = _np_cnf_to_int(cnf)

    sols = sat.itersolve(cnf)
    for sol in sols:
        _show_sol(sol)
    #print(" ".join('0' if i < 0 else '1' for i in sol))