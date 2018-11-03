#!usr/bin/python3

from moodle import Game
from time import time
from datetime import datetime
infinity = 999999999

def alphabeta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None): 
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    # Functions used by alphabeta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v
    
    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state, depth: depth > d or
                    game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -infinity
    beta = infinity
    best_action = None

    for a in game.actions(state):
        
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
        
        print("Action: ")
        print(a)
        print("Score: %f" % v)
      
    return best_action

fd=open('board.txt','r')
g=Game()

state=g.load_board(fd)
#test=state
#print(g.state["next_player"])
for line in state["board"]:
        print(line)

#print(g.actions(state))
'''
while (not g.terminal_test(state)):
    next=int(state["next_player"])
    print("next player: %d" % next)
    i=int(input("line: "))
    j=int(input("column: "))
    a=(next,i,j)
    state=g.result(state,a)
    print(g.terminal_test(state))
    next=int(g.to_move(state))
    print("Board: \n")
    for line in state["board"]:
        print(line)'''
################################################################################################################

finish = 0
action = ()
while not g.terminal_test(state):
    next=state["next_player"]
    print("next player: %d" % next)
    antes=time()
    if next==2:
        action = alphabeta_cutoff_search(state, g)
        state=g.result(state,action)

    if next==1:
        i=int(input("line: "))
        j=int(input("column: "))
        action=(next,i,j)
        #action = alphabeta_cutoff_search(state, g)
        state=g.result(state,action)
    depois=time()
    print(depois-antes) 
    print("Board: \n")
    for line in state["board"]:
        print(line)

print("Game Over!")
'''

antes=time()
g.actions(state)
depois=time()
print(depois-antes)

antes=time()
g.adjacents(1,1,4)
depois=time()
print(depois-antes) 

antes=time()
g.result(state,(1,1,1))
depois=time()
print(depois-antes)

antes=time()
g.utility(state,1)
depois=time()
print(depois-antes) 

antes=time()
g.terminal_test(state)
depois=time()
print(depois-antes)

antes=time()
g.winner(state)
depois=time()
print(depois-antes) '''
