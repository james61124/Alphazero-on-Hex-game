import math
import numpy as np

EPS = 1e-8

class MCTS():
    def __init__(self, game, nnet):
        self.game = game
        self.nnet = nnet
        self.Qsa = {}       # stores Q values for s,a (as defined in the paper)
        self.Nsa = {}       # stores the number of times s,a was visited
        self.Ns = {}        # stores the number of times s was visited
        self.Ps = {}        # stores initial policy (returned by neural net)

        self.Es = {}        # stores game.getGameEnded ended for board s
        self.Vs = {}        # stores game.getValidMoves for board s
        self.sim_count = 0
        self.number_of_simulations = 150
        self.eta = 1
        self.EPS = 1e-8

    def getActionProb(self, board, player, temp=1):
        """
        returns:
            probability of each valid action in this state
        """

        state_canonicalform = self.game.getCanonicalForm(board, player)

        for i in range(self.number_of_simulations):
            self.search(board, player)

        s = self.game.stringRepresentation(state_canonicalform)
        counts = [self.Nsa[(s,a)] if (s,a) in self.Nsa else 0 for a in range(self.game.getActionSize())]

        if temp==0:
            bestA = np.argmax(counts)
            probs = [0]*len(counts)
            probs[bestA]=1
            return probs

        probs = [x/float(sum(counts)) for x in counts]
        return probs


    def search(self, board, player):
        """
        return:
            the result(v) if doing the action 
        """

        self.sim_count += 1

        state_canonicalform = self.game.getCanonicalForm(board, player)
        s = self.game.stringRepresentation(state_canonicalform)
        if s not in self.Es: #store state to Es
            self.Es[s] = self.game.getGameEnded(state_canonicalform, 1)  # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        if self.Es[s]!=0: #if Es is ended, return its value
            return -self.Es[s]

        if s not in self.Ps: # stores initial policy (returned by neural net)
            self.Ps[s], v = self.nnet.predict(state_canonicalform)
            valids = self.game.getValidMoves(state_canonicalform, 1)
            self.Ps[s] = self.Ps[s]*valids # masking invalid moves
            sum_Ps_s = np.sum(self.Ps[s])
            if sum_Ps_s > 0:
                self.Ps[s] /= sum_Ps_s # normalize
            else:
                print("All valid moves were masked.")
                self.Ps[s] = self.Ps[s] + valids
                self.Ps[s] /= np.sum(self.Ps[s])

            self.Vs[s] = valids
            self.Ns[s] = 0
            return -v

        valids = self.Vs[s]
        cur_best = -float('inf')
        best_act = -1
        # find the best action by searching the max score
        for a in range(self.game.getActionSize()):
            if valids[a]:
                if (s,a) in self.Qsa:
                    score = self.Qsa[(s,a)] + self.eta*self.Ps[s][a]*math.sqrt(self.Ns[s])/(1+self.Nsa[(s,a)])
                else:
                    score = self.eta*self.Ps[s][a]*math.sqrt(self.Ns[s] + EPS)     # Q = 0 ?

                if score > cur_best:
                    cur_best = score
                    best_act = a
        a = best_act

        if valids[a]==0:
            print('invalid action in MCTS', a)
            assert valids[a] >0         

        next_state, _ = self.game.getNextState(state_canonicalform, 1, a)   
        next_state = self.game.getOriginalForm(next_state, player)
        next_player = -player 

        # the result (v) if doing the action 
        v = self.search(next_state, next_player)

        # If Qsa(s,a) is not visited, then Qsa(s,a) equals to v. 
        # However, doing the same action a in the same state s doesn’t mean that we will get the same result. 
        # If Qsa(s,a) was visited before, return the average of all the v.
        if (s,a) in self.Qsa:
            self.Qsa[(s,a)] = (self.Nsa[(s,a)]*self.Qsa[(s,a)] + v)/(self.Nsa[(s,a)]+1)
            self.Nsa[(s,a)] += 1

        else:
            self.Qsa[(s,a)] = v
            self.Nsa[(s,a)] = 1

        self.Ns[s] += 1
        return -v
