import copy
import time
from functools import reduce
import random


def get_checkers(state, player):
    return reduce(lambda all, p: all + (([p] if p.player == player else [])), list(filter(lambda p: p.captured == False, state.board.pieces)), [])

def heuristic(state):
    player1 = get_checkers(state, 1)
    player2 = get_checkers(state, 2)
    evaluation = 12*len(player1) - 12*len(player2)
    for p in player1:
        if p.king:
            evaluation += 8
        else:
            evaluation+= 1+ (p.position - 1)//4
            #evaluation_red += 5 + 2 + (piece.position - 1)//4
    for p in player2:
        if p.king:
            evaluation -= 8
        else:
            evaluation-= 8 - (p.position - 1)//4
    return evaluation


def find_move(state, time_left):
    start = time.time()
    player = state.whose_turn()
    moves = state.get_possible_moves()
    l = len(moves)
    if l == 1:
        return moves[0]
    if player == 1:
        heuristic = -1000000
    if player == 2:
        heuristic = 1000000
    move = random.choice(moves)
    alpha = -1000000
    beta = 1000000
    moves_left = 0
    for m in moves:
        state_copy = copy.deepcopy(state)
        state_copy.move(m)
        if time.time() - start >= time_left:
            return move
        time_left = time_left - (time.time() - start)
        val = minimax_search(state_copy, time_left / (l - moves_left), alpha, beta)
        moves_left+=1
        if player == 1:
            if val > heuristic:
                move = m
                heuristic = val
        if player == 2:
            if val < heuristic:
                move = m
                heuristic = val
    return move



def minimax_search(state, time_left, alpha, beta):
    start = time.time()
    player = state.whose_turn()
    moves = state.get_possible_moves()
    l = len(moves)
    cop = copy.deepcopy(state)
    if l == 0:
        return -999999
    cop.move(random.choice(moves))
    more = (cop.whose_turn() == state.whose_turn())
    if more:
        h = (-1) ** player * 1000000
    else:
        h = (-1) ** (player + 1) * 1000000
    moves_left = l
    for m in moves:
        state_copy = copy.deepcopy(state)
        state_copy.move(m)
        if time.time() - start >= time_left:
            return heuristic(state_copy)
        time_left = time_left - (time.time() - start)
        val = minimax_search(state_copy, time_left / moves_left, alpha, beta)
        moves_left -= 1
        if not more:
            if player == 1:
                if h > val:
                    h = val
            if player == 2:
                if h < val:
                    h = val
        if more:
            if player == 1:
                if h < val:
                    h = val
            if player == 2:
                if h > val:
                    h = val
        if player == 1:
            alpha = max(alpha, h)
        else:
            beta = min(beta, h)
        if beta < alpha:
            break
    return h
