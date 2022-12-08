from Hex import Hex
from internet_hex_bot import hex_bot
from baseline import MultiAgent

hexbot = hex_bot(1, 3, 0)
env = Hex()
method = MultiAgent(11, 1)

state = env.reset()
first_flag = 1
while not hexbot.is_done():
    if first_flag:
        action = 60
        first_flag = 0
    else:
        action = method.getMiniMaxAction(state)
    
    next_state, reward, done = env.step(state,action,1)
    state = next_state

    botmove = hexbot.agent_put(int(action))

    next_state, reward, done = env.step(state,botmove,-1)
    state = next_state