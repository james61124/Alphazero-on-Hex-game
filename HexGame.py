from __future__ import print_function
import sys
sys.path.append('..')
from HexLogic import Board
import numpy as np
from collections import defaultdict
from heapq import *


class Hex():
    def __init__(self, n=11):
        self.n = n

    def reset(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        return self.n*self.n

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        b = Board(self.n)
        b.pieces = np.copy(board)
        move = (int(action/self.n), action%self.n)
        b.execute_move(move, player)
        return (b.pieces, -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(board) 

        legalMoves =  b.get_legal_moves(player)
        if len(legalMoves)==0:
            print('no valid moves')
            return np.array(valids)
        for x, y in legalMoves:
            valids[self.n*x+y]=1
        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost

        b = Board(self.n)
        b.pieces = board

        for y in range(self.n):
            if b.is_connected((0, y), 1):
                return 1 if player == 1 else -1

        for x in range(self.n):
            if b.is_connected((x, 0), -1):
                return 1 if player == -1 else -1
        
        return 0            


    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        if player == 1:
            return board
        else:
            return np.fliplr(np.rot90(-1*board, axes=(1, 0)))

    def getOriginalForm(self, board, player):
        if player == 1:
            return board
        else:
            return np.rot90(np.fliplr(-1*board), axes=(0, 1))        
            
    def getSymmetries(self, board, pi):
        # rotation 180 degree
        assert(len(pi) == self.n**2)  # 1 for pass
        pi_board = np.reshape(pi, (self.n, self.n))
        l = []

        for i in [0, 2]:
            newB = np.rot90(board, i)
            newPi = np.rot90(pi_board, i)
            l += [(newB, list(newPi.ravel()))]
        return l

    def stringRepresentation(self, board):
        # 8x8 numpy array (canonical board)
        return board.tostring()
