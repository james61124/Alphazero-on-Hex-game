import numpy as np
#from pytorch_classification.utils import Bar, AverageMeter
import time
from tqdm import tqdm

class Arena():
    def __init__(self, player1, player2, game, display=None, mcts=None, ab=None):
        self.player1 = player1
        self.player2 = player2
        self.game = game
        self.display = display

        self.total_turn = 0
        self.mcts = mcts
        self.ab = ab

    def playGame(self):
        """
        returns:
            player who won the game (1 if player1, -1 if player2)
        """
        players = [self.player2, None, self.player1]
        curPlayer = 1
        board = self.game.reset()
        it = 0
        while self.game.getGameEnded(board, curPlayer)==0:          
            it+=1          
            action = players[curPlayer+1](board, curPlayer)
            board, _ = self.game.getNextState(self.game.getCanonicalForm(board, curPlayer), 1, action)
            board = self.game.getOriginalForm(board, curPlayer)
            curPlayer = -curPlayer
        self.total_turn += it                        
        return self.game.getGameEnded(board, 1)

    def playGames(self, num):
        """
        play several games
        return:
            how many times each player wins.
        """
        eps = 0

        num = int(num/2)
        oneWon = 0
        twoWon = 0
        draws = 0
        for _ in tqdm(range(num)):
            gameResult = self.playGame()
            if gameResult==1:
                oneWon+=1
            elif gameResult==-1:
                twoWon+=1
            else:
                draws+=1
            eps += 1

        self.player1, self.player2 = self.player2, self.player1
        
        for _ in tqdm(range(num)):
            gameResult = self.playGame()
            if gameResult==-1:
                oneWon+=1                
            elif gameResult==1:
                twoWon+=1
            else:
                draws+=1
            eps += 1

        return oneWon, twoWon, draws
