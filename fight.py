from game import game
from NNet import NNetWrapper
from MCTS import MCTS
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from HexGame import Hex
from baseline import MultiAgent
import matplotlib.pyplot as plt

env = Hex()
net = NNetWrapper(env)
game = game()
baseline = MultiAgent()
state = env.reset()
folder = ["./Tables/mcts25_1.pt","./Tables/mcts25_2.pt","./Tables/mcts25_3.pt","./Tables/mcts25_4.pt","./Tables/mcts25_5.pt"]
for w in range(5):
    net.nnet.load_state_dict(torch.load(folder[w]))
    player = -1
    actions = []
    p = []
    board_size =6
    table = ['A','B','C','D','E','F']
    print_out_action = []

    mcts = MCTS(env,net,25)
    wins = []
    main_wins = 0
    base_wins = 0
    print("iteration:",w)
    for i in range(100):
        state = env.reset()
        player = 1
        while True:
            
            action = np.argmax(mcts.getActionProb(state, player, temp=0))
            p.append(mcts.getActionProb(state, player, temp=1))
            action_tmp = [int(action/board_size),action%board_size]
            action_tmp2 = [table[int(action/board_size)],action%board_size]
            actions.append(action_tmp)
            print_out_action.append(action_tmp2)
            #print("main")
            #print(action_tmp)
            
            state, _ = env.getNextState(state, player, action)
            #print(state)
            if(env.getGameEnded(state,player)!=0):
                print("red win")
                wins.append("main")
                main_wins = main_wins + 1
                break
            state= np.reshape(state,board_size*board_size)

            player = -player
            #state= np.reshape(state,board_size*board_size)
            action = baseline.getMiniMaxAction(state)
            state= np.reshape(state,(board_size,board_size))
            state, _ = env.getNextState(state, player, action)
            action_tmp = [int(action/board_size),action%board_size]
            action_tmp2 = [table[int(action/board_size)],action%board_size]
            actions.append(action_tmp)
            print_out_action.append(action_tmp2)
            # print("base")
            # print(action_tmp)
            # print(state)
            if(env.getGameEnded(state,player)!=0):
                print("blue win")
                wins.append("base")
                base_wins = base_wins + 1
                break
            player = -player


            """
            state= np.reshape(state,board_size*board_size)
            action = baseline.getMiniMaxAction(state)
            state= np.reshape(state,(board_size,board_size))
            state, _ = env.getNextState(state, player, action)
            action_tmp = [int(action/board_size),action%board_size]
            action_tmp2 = [table[int(action/board_size)],action%board_size]
            # print("baseline")
            # print(action_tmp)
            # print(state)
            actions.append(action_tmp)
            print_out_action.append(action_tmp2)
            if(env.getGameEnded(state,player)!=0):
                print("red win")
                wins.append("base")
                game.display(actions,p)
                base_wins = base_wins + 1
                break
            player = -player

            # action = np.random.choice(36,1,mcts.getActionProb(state, player, temp=0))
            # action = action[0]
            # action_tmp = [int(action/board_size),action%board_size]
            # while state[int(action/board_size)][action%board_size]!=0:
            #     action = np.random.choice(36,1,mcts.getActionProb(state, player, temp=0))
            #     action = action[0]
            #     action_tmp = [int(action/board_size),action%board_size]
            #print(state)
            action = np.argmax(mcts.getActionProb(state, player, temp=0))
            p.append(mcts.getActionProb(state, player, temp=1))
            #print(type(p[0][0]))
            #print(p)
            action_tmp = [int(action/board_size),action%board_size]
            action_tmp2 = [table[int(action/board_size)],action%board_size]
            actions.append(action_tmp)
            print_out_action.append(action_tmp2)

            #print(action_tmp)
            state, _ = env.getNextState(state, player, action)
            #print(env.getGameEnded(state,player))
            if(env.getGameEnded(state,player)!=0):
                print("blue win")
                wins.append("main")
                main_wins = main_wins + 1
                break
            # print("main approach")
            # print(action_tmp)
            # print(state)
            state= np.reshape(state,board_size*board_size)
            player = -player
            """
        

    print(wins)
    print("main_wins: ",main_wins)
    print("base_wins: ",base_wins)
    #print(print_out_action)

