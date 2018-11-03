class Game():

    
    def to_move(self, s):

        """
        Returns the player to move next given the state s
        """

        return s["next_player"]

            
    def strings(self, board, player):   # builds a dictionary of strings at a given game state


        def in_dict(elem, dictionary):   # checks if a given coordinate [a, b] is already cointained in the dictionary of strings ..input..elem = [a, b]
            for key in dictionary:
                if elem in dictionary[key]:
                    return [1, key]   # contained
            return [0, 0] # not-contained

        count = 0
        all_strings = {}
        level = []
        board_size = len(board)
        
        for i in range(0, board_size):
            for j in range(0, board_size):
                if board[i][j] == player and in_dict([i, j], all_strings)[0] == 0:
                    count = 0
                    level = [[i, j]]
                    all_strings[str(i)+ str(j)] = [[level[0][0], level[0][1]]]
                    while True:
                        for adj in self.adjacents(level[0][0], level[0][1], board_size):
                            if board[adj[0]][adj[1]] == player and in_dict([adj[0], adj[1]], all_strings)[0] == 0:
                                all_strings[str(i)+ str(j)].append([adj[0], adj[1]])
                                level.append([adj[0], adj[1]])
                                count+=1
                        level.pop(0)
                        if level == []:
                            break
                                             
        return all_strings


    def winner(self, s):

        """
        Returns winning player. Note: does not account for draws
        : 1 for player 1
        : 2 for player 2
        : 0 for non terminal
        """

        strings_player_1 = self.strings(s["board"], 1)
        strings_player_2 = self.strings(s["board"], 2)
        board_size = len(s["board"])

        player_1_locked = False
        player_2_locked = False

        for (k, v) in strings_player_1.items():
            count = 0
            for elem in v:
                for (coord_1, coord_2) in self.adjacents(elem[0], elem[1], board_size):
                    if s["board"][coord_1][coord_2] == 0:
                        count+=1
                        break
                if count>0:
                    break
            if count == 0:
                player_1_locked = True

        for (k, v) in strings_player_2.items():
            count = 0
            for elem in v:
                for (coord_1, coord_2) in self.adjacents(elem[0], elem[1], board_size):
                    if s["board"][coord_1][coord_2] == 0:
                        count+=1
                        break
                if count>0:
                    break
            if count == 0:
                player_2_locked = True

        if player_1_locked and player_2_locked:
            # previous player locked itself to locker next player, so next player looses
            if s["next_player"] == 1:
                return 2
            else:
                return 1
        elif player_1_locked:
            return 2
        elif player_2_locked:
            return 1
        else:
            return 0


    def terminal_test(self, s): 

        """
        Returns a boolean of whether state s is terminal
        """

        if self.winner(s) == 0:
            return False
        else:
            return True

        
    def utility(self, s, p): 

        """
        Returns the payoff of state s if it is terminal
        (1 if p wins, -1 if p loses, 0 in case of a draw), otherwise, 
        its evaluation with respect to player p
        """
        winner = self.winner(s)
        
        if winner > 0:
            for line in s["board"]:
                if 0 in line:
                    if winner == p:
                        return 1
                    else:
                        return -1
            return 0

                        
        else:
            #return self.territory(s)
            return self.goncalo_utility(s["board"], p)

    def goncalo_utility(self, board, player):

        """
        Utiliy of goncalo when board is not in terminal phase - evaluation with respect to player p
        """

        N = len(board)
        zeros = 0
        liberties = 0

        for i in range(0, N):  
            for j in range(0, N):
                if board[i][j] == 0:
                    zeros+=1
                    for (coord_1, coord_2) in self.adjacents(i, j, N):
                        if board[coord_1][coord_2] == player:
                            liberties+=1
                            break
        
        return (liberties / zeros)

    def actions(self, s): 

        """
        Returns a list of valid moves at state s
        """
        
        board_size = len(s["board"])
        p = s["next_player"]
        actions = []
        
        for i in range(0, board_size):
            for j in range(0, board_size):
                if s["board"][i][j] == 0:
                    if 0 in self.adjacents2(i,j,s["board"]):
                        actions.append((p, i+1, j+1))
                    else:
                        winner = self.winner(self.result(s, (p, i+1,j+1)))
                        if winner >= 0:
                            if winner == p or winner == 0:
                                actions.append((p, i+1, j+1))
        return actions
        
    def adjacents(self, a, b, N):
        """
        Returns points surrounding a given (a,b) point
        """
        positions = []

        if a-1>=0:
            positions.append([a-1,b])
        if a+1<N:
            positions.append([a+1,b])
        if b-1>=0:
            positions.append([a,b-1])
        if b+1<N:
            positions.append([a,b+1])

        return positions

    def adjacents2(self, a, b, board):
        """
        Returns points surrounding a given (a,b) point
        """
        N=len(board[0])
        positions = []

        if a-1>=0:
            positions.append(board[a-1][b])
        if a+1<N:
            positions.append(board[a+1][b])
        if b-1>=0:
            positions.append(board[a][b-1])
        if b+1<N:
            positions.append(board[a][b+1])

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

        player = a[0]
        line = a[1]
        column = a[2]
        board = self.copy_board(s["board"])

        board[line - 1][column - 1] = player
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
                    board.append(list(map(int, line.replace('\n', ''))))
                else:
                    board_line = []
                    board.append(list(map(int, line.replace('\n', ''))))

            current_state = {
                "board": board,
                "next_player": next_player
            }
            print(board)
        except Exception as e:
            print('ERROR - load_board: {}'.format(e))

        return current_state