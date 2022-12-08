from collections import deque
from MCTS import MCTS
import numpy as np
from HexGame import Hex
from NNet import NNetWrapper as nn
import time, os, sys
from pickle import Pickler, Unpickler
from random import shuffle
from tqdm import tqdm
import torch
import torch.nn as nnn
import torch.nn.functional as F
from Arena import Arena



class Coach():
    def __init__(self):
        self.env = Hex()
        self.nnet = nn(self.env)
        self.pnet = self.nnet.__class__(self.env) 
        self.mcts = MCTS(self.env, self.nnet)
        self.history_training_example = []   
        self.skipFirstSelfPlay = False
        self.number_of_history_training_example = 20
        self.learning_iteration = 15  #要練幾次
        self.selfplay_iteration = 300 #自己跟自己打架要幾次
        self.testing_iteration = 100 #試的時候要要打架幾次
        self.tempThreshold = 15

    def executeEpisode(self):
        """
        return (state_canonicalboard,pi,v)
        pi is the probability of all valid action produced from policy network
        v is 1 if the player eventually wins the game, else -1
        """
        trainExamples = []
        state = self.env.reset()
        self.curPlayer = 1
        episodeStep = 0

        while True:
            episodeStep += 1
            state_canonicalform = self.env.getCanonicalForm(state, self.curPlayer)
            #temp = int(episodeStep < self.tempThreshold)
            #pi = self.mcts.getActionProb(state, self.curPlayer, temp=temp)
            pi = self.mcts.getActionProb(state, self.curPlayer)
            sym = self.env.getSymmetries(state_canonicalform, pi)
            for b,p in sym:
                trainExamples.append([b, self.curPlayer, p, None]) #state player 
            action = np.random.choice(len(pi), p=pi) # weighted random

            state, _ = self.env.getNextState(state_canonicalform, 1, action)
            state = self.env.getOriginalForm(state, self.curPlayer)
            self.curPlayer = -self.curPlayer

            r = self.env.getGameEnded(state, self.curPlayer)

            if r!=0:
                return [(x[0],x[2],r*((-1)**(x[1]!=self.curPlayer))) for x in trainExamples] #state probability player

    def learn(self):
        """
        Performs numIters iterations with numEps episodes of self-play in each
        iteration. After every iteration, it retrains neural network with
        examples in trainExamples (which has a maximium length of maxlenofQueue).
        It then pits the new neural network against the old one and accepts it
        only if it wins >= updateThreshold fraction of games.
        """

        for i in range(self.learning_iteration):
            print('------ITER ' + str(i) + '------')
            print("self play")
            training_example = []
            for eps in tqdm(range(self.selfplay_iteration)):
                self.mcts = MCTS(self.env, self.nnet)   # reset search tree
                training_example += self.executeEpisode()

            self.history_training_example.append(training_example)

            if len(self.history_training_example) > self.number_of_history_training_example: 
                self.history_training_example.pop(0)
            self.save_train_examples()

            trainExamples = []
            for e in self.history_training_example:
                trainExamples.extend(e)
            shuffle(trainExamples) 
            print("number of trainExamples: ",len(trainExamples))

            folder = "./Tables/DQN.pt"
            if not os.path.exists(folder):
                print("new_trained_model")
                torch.save(self.nnet.nnet.state_dict(), "./Tables/DQN.pt")
                self.pnet.nnet.load_state_dict(self.nnet.nnet.state_dict())
            else:
                print("load_old_trained_model")
                self.nnet.nnet.load_state_dict(torch.load( "./Tables/DQN.pt"))
                self.pnet.nnet.load_state_dict(torch.load( "./Tables/DQN.pt"))

            pmcts = MCTS(self.env, self.pnet)
            self.nnet.train(trainExamples)
            nmcts = MCTS(self.env, self.nnet)
            pwins = 0
            nwins = 0

            arena = Arena(lambda x, player: np.argmax(pmcts.getActionProb(x, player, temp=0)),
                          lambda x, player: np.argmax(nmcts.getActionProb(x, player, temp=0)), self.env)
            pwins, nwins, draws = arena.playGames(self.testing_iteration)

            if pwins+nwins > 0 and float(nwins)/(pwins+nwins) < 0.6 :
                print('REJECTING NEW MODEL')
                print(nwins,"/",pwins+nwins)
            else:
                print('ACCEPTING NEW MODEL')
                torch.save(self.nnet.nnet.state_dict(), "./Tables/DQN.pt")
                print(nwins,"/",pwins+nwins)

    def save_train_examples(self):
        folder = "./previous_models/"
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = os.path.join(folder, "previous_model_11.pth.tar")
        with open(filename, "wb+") as f:
            Pickler(f).dump(self.history_training_example)
        f.closed

    def load_train_examples(self):
        modelFile = os.path.join("./previous_models/", "previous_model_11.pth.tar")
        if not os.path.isfile(modelFile):
            sys.exit()
        else:
            with open(modelFile, "rb") as f:
                self.history_training_example = Unpickler(f).load()
            f.closed
            # examples based on the model were already collected (loaded)
            self.skipFirstSelfPlay = True