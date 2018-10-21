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
        return best_action
    
class Game():

    def __init__(self, board_file):

        try:
            with open(board_file, 'r+') as file:
                
                self.state = self.load_board(file)

        except Exception as e:
            print('__init__: {}'.format(e))
            return

    def to_move(self, s):

        """
        Returns the player to move next given the state s
        """
        
        if s["next_player"] == 1:
            s["next_player"] = 2;
        elif s["next_player"] == 2:
            s["next_player"] = 1;

        return s["next_player"]

    def terminal_test(self, s): 

        """
        Returns a boolean of whether state s is terminal
        """

        def adjacents(a, b, state):   # returns all possible adjacents positions for the position [a, b] in the game board

            positions = [];

            if a == 0 and b == 0:
                positions.extend([[a + 1, b], [a, b + 1]]);
                return positions;
            elif a == state["board size"] - 1 and b == state["board size"] - 1:
                positions.extend([[a, b - 1], [a - 1, b]]);
                return positions;
            elif a == 0 and b == state["board size"] - 1:
                positions.extend([[0, b - 1], [a + 1, b]]);
                return positions;
            elif a == state["board size"] - 1 and b == 0:
                positions.extend([[a - 1, 0], [a, b + 1]]);
                return positions;
            elif a == 0:
                positions.extend([[a, b + 1], [a, b - 1], [a + 1, b]]);
                return positions;
            elif a == state["board size"] - 1:
                positions.extend([[a, b + 1], [a, b - 1], [a - 1, b]]);
                return positions;
            elif b == 0:
                positions.extend([[a - 1, b], [a + 1, b], [a, b + 1]]);
                return positions;
            elif b == state["board size"] - 1:
                positions.extend([[a - 1, b], [a + 1, b], [a, b - 1]]);
                return positions;
            else:
                positions.extend([[a - 1, b], [a + 1, b], [a, b - 1], [a, b + 1]]);
                return positions;

        def in_dict(elem, dictionary):   # checks if a given coordinate [a, b] is already cointained in the dictionary of strings ..input..elem = [a, b] 
            for key, value in dictionary.items():
                for array in value:
                    if elem == array:
                        return [1, key]
            return [0, 0]
            
        def strings(state):   # builds a dictionary of the strings at a given game state
            
            count = 0;
            all_strings = {};
            level = [];
            
            for i in range(0, state["board size"]):
                for j in range(0, state["board size"]):
                    if state["board"][i][j] == str(state["next player"]) and in_dict([i, j], all_strings)[0] == 0:
                        count = 0;
                        level = [[i, j]];
                        all_strings[str(i)+ str(j)] = [[level[0][0], level[0][1]]]
                        while True:
                            for adj in adjacents(level[0][0], level[0][1], state):
                                if state["board"][adj[0]][adj[1]] == str(state["next player"]) and in_dict([adj[0], adj[1]], all_strings)[0] == 0:
                                    all_strings[str(i)+ str(j)].append([adj[0], adj[1]]);
                                    level.append([adj[0], adj[1]])
                                    count+=1;
                            level.pop(0);
                            if level == []:
                                break
                                                 
            return all_strings;
            
        dict_of_strings = strings(s);
        print(dict_of_strings)

        for (k, v) in dict_of_strings.items():
            count = 0;
            for elem in v:
                for (coord_1, coord_2) in adjacents(*elem, s):
                    if s["board"][coord_1][coord_2] == '0':
                        count+=1
                        break
            if count == 0:
                return 0;     # terminal state
                
        return 1;     #non-terminal state       
        
    def utility(self, s, p): 

        """
        Returns the payoff of state s if it is terminal
        (1 if p wins, -1 if p loses, 0 in case of a draw), otherwise, 
        its evaluation with respect to player p
        """
    def actions(self, s): 

        """
        Returns a list of valid moves at state s
        """
    def result(self, s, a):

        """
        returns the sucessor game state after playing move a at state s
        """
        
    def load_board(self, file_stream):

        """ 
        It loads the board, given an opened file stream with the specifications.

        Example content of file:
        4 1
        0010
        0122
        0210
        0000
        """

        current_state = {}

        try:
            board_size, next_player = [int(x) for x in next(file_stream).split()] # read first line
            board = []
            first_line = True
            for line in file_stream: # read rest of lines
                if first_line:
                    first_line = False
                    board.append(list(line.replace('\n', '')))
                else:
                    board_line = []
                    board.append(list(line.replace('\n', '')))

            current_state = {
                "board": board,
                "next player": next_player,
                "board size": board_size
            }

        except Exception as e:
            print('ERROR - load_board: {}'.format(e))

        return current_state

################################################################################################################

atari_go = Game("initial_state.txt");
atari_go.terminal_test(atari_go.state);
