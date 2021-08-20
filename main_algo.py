import numpy as np
from pysat.solvers import Glucose3
import itertools
# from read_input import *
import time


SWAP_SIGN = -1
# board = readFile("input_10x10.txt")
# print(board)

# n là len(board) số dòng
# m là len(board[0]) số cột


def gen_moves(i, j, n, size):
    if i == 0 and j == 0:                                                         # top-left corner
        return [0, 1, size, size + 1]
    elif i == 0 and j == size - 1:                                                # top-right corner
        return [-1, 0, size - 1, size]
    elif i == n - 1 and j == 0:                                                # bot-left corner
        return [-size, -size + 1, 0, 1]
    elif i == n - 1 and j == size - 1:                                         # bot-right corner
        return [-size - 1, -size, -1, 0]
    elif i == 0:                                                                  # top edge
        return [-1, 0, +1, size - 1, size, size + 1]
    elif i == n - 1:                                                           # bot edge
        return [-size - 1, -size, -size + 1, -1, 0, 1]
    elif j == 0:                                                                  # left edge
        return [-size, -size + 1, 0, 1, size, size + 1]
    elif j == size - 1:                                                           # right edge
        return [-size - 1, -size, - 1, 0, size - 1, size]
    else:                                                                         # center
        return [-size - 1, -size, -size + 1, -1, 0, 1, size - 1, size, size + 1]


def get_clause(i, j, value, size, n):
    position = i * size + j + 1
    moves = gen_moves(i, j, n, size)
    clause = []
    if value > len(moves):
        for move in moves:
            clause.append([position + move])
    else:
        t = (position + np.array(moves))
        r = list(itertools.combinations(t, value + 1))
        cl = np.asarray(r)
        clause.extend(cl * -1)
        temp = position + np.array(moves)
        r = list(itertools.combinations(temp, len(moves) - value + 1))
        cl = np.asarray(r)
        clause.extend(cl)
    return clause


def init_clause(board):
    clauses = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] >= 0:
                clauses += get_clause(i, j,
                                      board[i][j], len(board[0]), len(board))
    # print('#clauses:', clauses)
    return clauses


def pySAT_coloring(board):
    clauses = init_clause(board)
    g = Glucose3()
    for it in clauses:
        g.add_clause([int(k) for k in it])
    # print(g.solve())
    g.solve()
    model = g.get_model()
    # print(model)
    # print(board, end='\n')

    pySAT_result = np.ones((len(board), len(board[0])))

    for i in range(len(board)):
        for j in range(len(board[0])):
            if i * len(board[0]) + j + 1 not in model:
                pySAT_result[i][j] = 0
    return pySAT_result


# result = pySAT_coloring(readFile("input_10x10.txt"))


def Brute_force(CNF):
    literals = set()
    for conj in CNF:
        for disj in conj:
            literals.add(abs(disj))
    literals = list(literals)
    n = len(literals)
    for seq in itertools.product([1, -1], repeat=n):
        a = np.asarray(seq) * np.asarray(literals)
        if all([bool(set(disj).intersection(set(a))) for disj in CNF]):
            return True, a
    return False, None


# a = Brute_force(init_clause(board))
# print(a)


def BF_coloring(board):
    TF, model = Brute_force(init_clause(board))

    BF_result = np.ones((len(board), len(board[0])))
    for i in range(len(board)):
        for j in range(len(board[0])):
            if i * len(board[0]) + j + 1 not in model:
                BF_result[i][j] = 0
    return BF_result


# print(BF_coloring(board))

def select_literal(cnf):
    for c in cnf:
        for literal in c:
            return literal


def dpll(cnf, assignments=[]):
    if len(cnf) == 0:
        return True, assignments

    if any([len(c) == 0 for c in cnf]):
        return False, None

    l = select_literal(cnf)
    new_cnf = [c for c in cnf if l not in c]
    temp = []
    for c in new_cnf:
        if -l in c:
            c = c[c != -l]
        temp.append(c)
    t = assignments.copy()
    t.append(l)
    sat, vals = dpll(temp, t)
    if sat:
        return sat, vals
    else:
        t.remove(l)

    new_cnf = [c for c in cnf if -l not in c]
    temp = []
    for c in new_cnf:
        if l in c:
            c = c[c != l]
        temp.append(c)
    t = assignments.copy()
    t.append(-l)
    sat, vals = dpll(temp, t)
    if sat:
        return sat, vals
    else:
        t.remove(-l)
    return False, None


def Backtracking_coloring(board):
    sol, model = dpll(init_clause(board))

    Backtracking_result = np.ones((len(board), len(board[0])))
    for i in range(len(board)):
        for j in range(len(board[0])):
            if i * len(board[0]) + j + 1 not in model:
                Backtracking_result[i][j] = 0
    return Backtracking_result

# Code to count time
# Brute Force
# print('Brute Force')
# t0 = time.time()
# print(BF_coloring(board))
# t1 = time.time()
# print('Time:', t1 - t0)

# pySAT
# print('pySAT')
# t2 = time.time()
# print(pySAT_coloring(board))
# t3 = time.time()
# print('Time:', t3 - t2)

# Backtracking
# print('Backtracking')
# t4 = time.time()
# print(Backtracking_coloring(board))
# t5 = time.time()
# print('Time:', t5 - t4)
