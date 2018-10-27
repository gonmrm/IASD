
class Game():


    def to_move(self, s):

        """
        Returns the player to move next given the state s
        """

        return s["next_player"]

    def terminal_test(self, s): 

        """
        Returns a boolean of whether state s is terminal
        """


        def in_dict(elem, dictionary):   # checks if a given coordinate [a, b] is already cointained in the dictionary of strings ..input..elem = [a, b] 
            for key, value in dictionary.items():
                for array in value:
                    if elem == array:
                        return [1, key]
            return [0, 0]
            
        def strings(state):   # builds a dictionary of the strings at a given game state
            
            count = 0
            all_strings = {}
            level = []
            board_size = len(state["board"])
            
            for i in range(0, board_size):
                for j in range(0, board_size):
                    if state["board"][i][j] == str(state["next_player"]) and in_dict([i, j], all_strings)[0] == 0:
                        count = 0
                        level = [[i, j]]
                        all_strings[str(i)+ str(j)] = [[level[0][0], level[0][1]]]
                        while True:
                            for adj in self.adjacents(level[0][0], level[0][1], state):
                                if state["board"][adj[0]][adj[1]] == str(state["next_player"]) and in_dict([adj[0], adj[1]], all_strings)[0] == 0:
                                    all_strings[str(i)+ str(j)].append([adj[0], adj[1]])
                                    level.append([adj[0], adj[1]])
                                    count+=1
                            level.pop(0)
                            if level == []:
                                break
                                                 
            return all_strings
            
        dict_of_strings = strings(s)

        for (k, v) in dict_of_strings.items():
            count = 0
            for elem in v:
                for (coord_1, coord_2) in self.adjacents(elem[0], elem[1], s):
                    if s["board"][coord_1][coord_2] == '0':
                        count+=1
                        break
            if count == 0:
                return True     # terminal state
                
        return False     #non-terminal state       
        
    def utility(self, s, p): 

        """
        Returns the payoff of state s if it is terminal
        (1 if p wins, -1 if p loses, 0 in case of a draw), otherwise, 
        its evaluation with respect to player p
        """

        board_size = len(s["board"])

        if self.terminal_test(s):
            for i in range(0, board_size):
                for j in range(0, board_size):
                    if s["board"][i][j] == 0:
                        if self.to_move(s) == p:
                            return -1
                        else:
                            return 1
            return 0
                        
        else:
            return 2
            
    def actions(self, s): 

        """
        Returns a list of valid moves at state s
        """
        p = s["next_player"]
        board = s["board"]
        i = 1
        j = 1
        actions=[]
        state = {"board":board, "next_player":p}
        
        for line in board:
            for point in line:
                if point == str(0):
                    adj = self.adjacents(i - 1, j - 1, s)
                    if type(adj) is list:
                        for place in adj:
                            if board[place[0]][place[1]] == str(0):
                                actions.append((p,i,j))
                            else:
                                test_state=self.result(state,(p,i,j))
                                if self.terminal_test(test_state):
                                    actions.append((p,i,j))

                j+=1
            j = 1
            i+=1

            
        return actions

    def adjacents(self, a, b, state):
        """
        Returns points surrounding a given (a,b) point
        """
        N = len(state["board"])
        positions = []

        if a == 0 and b == 0:       # Upper left corner
            positions.extend([[a + 1, b], [a, b + 1]])
            return positions
        elif a == N-1 and b == N-1:     # Bottom right corner
            positions.extend([[a, b - 1], [a - 1, b]])
            return positions
        elif a == 0 and b == N-1:     # Upper right corner
            positions.extend([[a, b - 1], [a + 1, b]])
            return positions
        elif a == N-1 and b == 0:     # Bottom left corner
            positions.extend([[a - 1, b], [a, b + 1]])
            return positions
        elif a > N-1 or b > N-1:
            print("Position does not exist in board!!") # Impossible cases
            return 0
        elif a == 0:                # Upper side
            positions.extend([[a, b + 1], [a, b - 1], [a + 1, b]])
            return positions
        elif a == N-1:                # Bottom side
            positions.extend([[a, b + 1], [a, b - 1], [a - 1, b]])
            return positions
        elif b == 0:                # Left side
            positions.extend([[a - 1, b], [a + 1, b], [a, b + 1]])
            return positions
        elif b == N-1:                # Right side
            positions.extend([[a - 1, b], [a + 1, b], [a, b - 1]])
            return positions
        else:                       # Every other case
            positions.extend([[a - 1, b], [a + 1, b], [a, b - 1], [a, b + 1]])
            return positions



    def copy_board(self, board):

        """
        It will copy board element by element, not returning a pointer but a new board in memory
        """
        new_board = []

        for line in board:
            new_board.append([])
            for point in line:
                new_board[-1].append(point)

        return new_board



    def result(self, s, a):

        """
        returns the sucessor game state after playing move a at state s
        """

        player  = a[0]
        line = a[1]
        column = a[2]
        board = self.copy_board(s["board"])

        board[line - 1][column - 1] = str(player)
        if player == 1:
            next_player = 2
        else:
            next_player = 1

        return {
            "board": board,
            "next_player": next_player
        }
        
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
                "next_player": next_player
            }

        except Exception as e:
            print('ERROR - load_board: {}'.format(e))

        return current_state

