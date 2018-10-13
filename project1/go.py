class Game():

    def __init__(self, board_file):

        try:
            with open(board_file, 'r+') as file:
                
                self.state = self.load_board(file)

        except Exception as e:
            print('__init__: {}'.format(e))
            return

        


    def to_move(self, state):

        """
        Returns the player to move next given the state s
        """

        return state["next_player"]



    def terminal_test(self, s): 

        """
        Returns a boolean of whether state s is terminal
        """

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
                else:
                    board_line = []
                    board_line.append(line)
                    board.append(board_line)

            current_state = {
                "board": board,
                "next_player": next_player
            }

        except Exception as e:
            print('ERROR - load_board: {}'.format(e))

        return current_state

