import numpy as np
import sys
sys.path.append('../../')

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from tqdm import tqdm

from HexNNet import HexNNet as hnnet

class NNetWrapper():
    def __init__(self, game):
        self.nnet = hnnet(game)
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.numEps = 15
        self.batch_size = 64

    def train(self, trainExamples):
        """
        examples: list of examples, each example is of form (board, pi, v)
        """
        optimizer = optim.Adam(self.nnet.parameters())
        for epoch in tqdm(range(self.numEps)):
            batch_idx = 0
            while batch_idx < int(len(trainExamples)/self.batch_size):
                sample_ids = np.random.randint(len(trainExamples), size=self.batch_size)
                state, pis, vs = list(zip(*[trainExamples[i] for i in sample_ids]))
                state = torch.FloatTensor(np.array(state).astype(np.float64))
                target_pis = torch.FloatTensor(np.array(pis))
                target_vs = torch.FloatTensor(np.array(vs).astype(np.float64))

                out_pi, out_v = self.nnet(state)
                l_pi = self.loss_pi(target_pis, out_pi)
                l_v = self.loss_v(target_vs, out_v)

                total_loss = l_pi + l_v
                #print("total_loss: ",total_loss)
                optimizer.zero_grad()
                total_loss.backward()
                optimizer.step()
                batch_idx += 1

    def predict(self, board):
        board = torch.FloatTensor(board.astype(np.float64))
        board = board.view(1, self.board_x, self.board_y) #resize
        self.nnet.eval() #不啟用Batch Normalization 和 Dropout
        with torch.no_grad():            
            pi, v = self.nnet(board)
        return torch.exp(pi).data.cpu().numpy()[0], v.data.cpu().numpy()[0]

    def loss_pi(self, targets, outputs):
        return -torch.sum(targets*outputs)/targets.size()[0]

    def loss_v(self, targets, outputs):
        return torch.sum((targets-outputs.view(-1))**2)/targets.size()[0]

