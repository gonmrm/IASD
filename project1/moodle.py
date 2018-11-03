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
        index = 0
        for i in range(0, board_size):
            for j in range(0, board_size):
                if board[i][j] == player and in_dict([i, j], all_strings)[0] == 0:
                    count = 0
                    level = [(i, j)]
                    all_strings[index] = [(level[0][0], level[0][1])]
                    while True:
                        for adj in self.adjacents(level[0][0], level[0][1], board_size):
                            if board[adj[0]][adj[1]] == player and in_dict([adj[0], adj[1]], all_strings)[0] == 0:
                                all_strings[index].append((adj[0], adj[1]))
                                level.append((adj[0], adj[1]))
                                count+=1
                        level.pop(0)
                        if level == []:
                            break
                index+=1
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

        for v in strings_player_1.values():
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

        for v in strings_player_2.values():
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
            return self.rui(s["board"],p)
<<<<<<< HEAD
=======
            #return 0.5
>>>>>>> 2c1e201ddc5241e16101ac287393d571a4c2eba8
            #return self.goncalo_utility(s["board"], p)

    def rui(self,board,player):
        if player == 1:
            other = 2
        else:
            other = 1
        N=len(board)
        score = 0.5
        for i in range(0, N):  
            for j in range(0, N):
                if board[i][j] == other:
                    for point in self.adjacent_values(i,j,board):
                        if point == 0:
                            score-=0.01
                '''if board[i][j] == player:
                    for point in self.adjacent_values(i,j,board):
                        if point == 0:
                            score+=0.01'''
        return score
    def goncalo_utility(self, board, player):

        """
        Utiliy of goncalo when board is not in terminal phase - evaluation with respect to player p
        """

        #strings_player = self.strings(board, player)

        if player == 1:
            other = 2
        else:
            other = 1

        N = len(board)
        zeros = 0
        liberties_player = 0
        liberties_other = 0
        liberties_player_increment = True
        liberties_other_increment = True

        for i in range(0, N):  
            for j in range(0, N):
                if board[i][j] == 0:
                    zeros+=1
                    for (coord_1, coord_2) in self.adjacents(i, j, N):
                        if board[coord_1][coord_2] == player and liberties_player_increment:
                            liberties_player+=1
                            liberties_player_increment = False
                        elif board[coord_1][coord_2] == other and liberties_other_increment:
                            liberties_other+=1
                            liberties_other_increment = False
                    liberties_player_increment = True
                    liberties_other_increment = True
        
        return (liberties_player - 3*liberties_other) / (zeros*5)

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
                    if 0 in self.adjacent_values(i, j, s["board"]):
                        actions.append((p, i+1, j+1))
                    else:
                        winner = self.winner(self.result(s, (p, i+1,j+1)))
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

    def adjacent_values(self, a, b, board):
        """
        Returns values surrounding a given (a,b) point
        """

        N = len(board)
        values = []

        if a-1>=0:
            values.append(board[a-1][b])
        if a+1<N:
            values.append(board[a+1][b])
        if b-1>=0:
            values.append(board[a][b-1])
        if b+1<N:
            values.append(board[a][b+1])

        return values
        

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

        #player = a[0]
        #line = a[1]
        #column = a[2]
        board = self.copy_board(s["board"])

        board[a[1] - 1][a[2] - 1] = a[0]
        if a[0] == 1:
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
