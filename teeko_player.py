import random
import copy


class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']
    
    

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]
        
    def max_val(self, state, deep, drop_phase):
        val = self.game_value(state)
        if(val == 1 or val == -1):
            return val, state
        elif(deep >= 3):
            return self.heuristic_game_value(state),state
        else:
            a = -1000
            allSucc = self.succ(state, drop_phase, self.my_piece)
            ret = None
            for eachSucc in allSucc:
                temp = a
                b, st = self.min_val(eachSucc, deep + 1,drop_phase)
                #print(a)
                #print(b)
                a = max(a, b)
                if(a != temp):
                    #print("goes here")
                    ret = eachSucc
                    #print(ret)
        return a,ret
    
    def min_val(self, state, deep,drop_phase):
        val = self.game_value(state)
        if(val == 1 or val == -1):
            return val, state
        elif(deep >= 3):
            return self.heuristic_game_value(state),state
        else:
            b = 1000
            allSucc = self.succ(state, drop_phase, self.my_piece)
            ret = None
            for eachSucc in allSucc:
                temp = b
                a, st = self.max_val(eachSucc, deep + 1,drop_phase)
                b = min(a, b)
                if(b != temp):
                    ret = eachSucc
        return b,ret
            
            
    def succ(self,state, drop, piece):
        #print(state)
        #print(piece)
        succList = []
        if(drop == True):
            for row in range(len(state)):
                for cell in range(len(state[row])):
                    succState = copy.deepcopy(state)
                    if(succState[row][cell] == ' '):
                        succState[row][cell] = piece
                        succList.append(succState)
        else:
            for row in range(len(state)):
                for cell in range(len(state[row])):
                    succState = copy.deepcopy(state)
                    if(succState[row][cell] == piece):
                        i = row
                        j = cell
                        #8 cases check
                        succState = copy.deepcopy(state)
                        if((i + 1) < len(succState) and succState[i + 1][j] == ' '):
                            succState[i + 1][j] = piece
                            succState[i][j] = ' '
                            succList.append(succState)
                        succState = copy.deepcopy(state)
                        if((j + 1) < len(succState[row]) and succState[i][j + 1] == ' '):
                            succState[i][j + 1] = piece
                            succState[i][j] = ' '
                            succList.append(succState)
                        succState = copy.deepcopy(state)
                        if((i - 1) >= 0 and succState[i - 1][j] == ' '):
                            succState[i - 1][j] = piece
                            succState[i][j] = ' '
                            succList.append(succState)
                        succState = copy.deepcopy(state)
                        if((j - 1) >= 0 and succState[i][j - 1] == ' '):
                            succState[i][j - 1] = piece
                            succState[i][j] = ' '
                            succList.append(succState)
                        succState = copy.deepcopy(state)
                        if((j - 1) >= 0 and  (i - 1) >=0 and succState[i - 1][j - 1] == ' '):
                            succState[i - 1][j - 1] = piece
                            succState[i][j] = ' '
                            succList.append(succState)
                        succState = copy.deepcopy(state)
                        if((j + 1) < len(succState[row]) and  (i + 1) < len(succState) and succState[i + 1][j + 1] == ' '):
                            succState[i + 1][j + 1] = piece
                            succState[i][j] = ' '
                            succList.append(succState)
                        succState = copy.deepcopy(state)
                        if((j + 1) < len(succState[row]) and  (i - 1) >= 0 and succState[i - 1][j + 1] == ' '):
                            succState[i - 1][j + 1] = piece
                            succState[i][j] = ' '
                            succList.append(succState)
                        succState = copy.deepcopy(state)
                        if((j - 1) >= 0 and  (i + 1) < len(succState) and succState[i + 1][j - 1] == ' '):
                            succState[i + 1][j - 1] = piece
                            succState[i][j] = ' '
                            succList.append(succState)
        return succList
        
    def make_move(self, state):
        #print("Hola")
        #print(self.my_piece)
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.
        
        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.
                
                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).
        
        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        #Check drop phase
        drop_phase = False
        count = 0
        for row in range(len(state)):
            for cell in range(len(state[row])):
                if(state[row][cell] != ' '):
                    count = count + 1
        if(count < 8):
            drop_phase = True
        else:
            drop_phase = False
        
        val, successor = self.max_val(state, 0, drop_phase)
        #print('SUCCESSOR IS', successor)
        move =[]
        stup = ()
        ntup = ()
        for row in range(len(state)):
            for cell in range(len(state[row])):
                if(successor[row][cell] != state[row][cell]):
                    if(state[row][cell] == self.my_piece):
                        stup = (row,cell)
                    if(successor[row][cell] == self.my_piece):
                        ntup = (row,cell)
        move.append(ntup)
        if(stup != ()):
            move.append(stup)
        return move
            
        
        #print(succList)
        #if not drop_phase:
            # : choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            #pass

        # select an unoccupied space randomly
        #  implement a minimax algorithm to play better
        """
        move = []
        (row, col) = (random.randint(0,4), random.randint(0,4))
        while not state[row][col] == ' ':
            (row, col) = (random.randint(0,4), random.randint(0,4))
            
        # ensure the destination (row,col) tuple is at the beginning of the move list
        move.insert(0, (row, col))
        return move
        """
    
    def heuristic_game_value(self,state):
        if(self.game_value(state) == 1 or self.game_value(state) == -1):
            h = self.game_value(state)
            return h
        h = 0
        #for i in range(len(state)):
            #print(state[i])
        
        #check down
        for row in range(len(state)):
            for cell in range(len(state[row])):
                if(state[row][cell] == self.my_piece):
                    th = 1
                    down = row + 1
                    while(down < len(state)):
                        if(state[down][cell] == self.my_piece):
                            th = th + 1
                        else:
                            break
                        down = down + 1
                    if(th > h):
                        h = th
        #check right
        for row in range(len(state)):
            for cell in range(len(state[row])):
                if(state[row][cell] == self.my_piece):
                    th = 1
                    right = cell + 1
                    while(right < len(state[row])):
                        if(state[row][right] == self.my_piece):
                            th = th + 1
                        else:
                            break
                        right = right + 1
                    if(th > h):
                        h = th
        
                        
        #check right down
        for row in range(len(state)):
            for cell in range(len(state[row])):
                if(state[row][cell] == self.my_piece):
                    th = 1
                    down = row + 1
                    right = cell + 1
                    while(down < len(state) and right < len(state[row])):
                        if(state[down][right] == self.my_piece):
                            th = th + 1
                        else:
                            break
                        right = right + 1
                        down = down + 1
                    if(th > h):
                        h = th
        
        # check left down
        for row in range(len(state)):
            for cell in range(len(state[row])):
                if(state[row][cell] == self.my_piece):
                    th = 1
                    down = row + 1
                    left = cell - 1
                    while(down < len(state) and left >= 0):
                        if(state[down][left] == self.my_piece):
                            th = th + 1
                        else:
                            break
                        left = left - 1
                        down = down + 1
                    if(th > h):
                        h = th
                        
        #opposition
        hopp = 0              
        #check down
        for row in range(len(state)):
            for cell in range(len(state[row])):
                if(state[row][cell] == self.opp):
                    th = 1
                    down = row + 1
                    while(down < len(state)):
                        if(state[down][cell] == self.opp):
                            th = th + 1
                        else:
                            break
                        down = down + 1
                    if(th > hopp):
                        hopp = th
        #check right
        for row in range(len(state)):
            for cell in range(len(state[row])):
                if(state[row][cell] == self.opp):
                    th = 1
                    right = cell + 1
                    while(right < len(state[row])):
                        if(state[row][right] == self.opp):
                            th = th + 1
                        else:
                            break
                        right = right + 1
                    if(th > hopp):
                        hopp = th
        
                        
        #check right down
        for row in range(len(state)):
            for cell in range(len(state[row])):
                if(state[row][cell] == self.opp):
                    th = 1
                    down = row + 1
                    right = cell + 1
                    while(down < len(state) and right < len(state[row])):
                        if(state[down][right] == self.opp):
                            th = th + 1
                        else:
                            break
                        right = right + 1
                        down = down + 1
                    if(th > hopp):
                        hopp = th
        
        # check left down
        for row in range(len(state)):
            for cell in range(len(state[row])):
                if(state[row][cell] == self.opp):
                    th = 1
                    down = row + 1
                    left = cell - 1
                    while(down < len(state) and left >= 0):
                        if(state[down][left] == self.opp):
                            th = th + 1
                        else:
                            break
                        left = left - 1
                        down = down + 1
                    if(th > hopp):
                        hopp = th
        
        #print("AI Score", h)
        #print("player scor", hopp)
        #return (h - hopp)/4
    
        if(h >= hopp):
            return h/4
        else:
            return -hopp/4
            
                

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        #print(move)
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                raise Exception("You don't have a piece there!")
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)
        
    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece
        
        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
                
                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece
        
    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")
        
    def game_value(self, state):
        """ Checks the current board status for a win condition
        
        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        complete checks for diagonal and 2x2 box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # check \ diagonal wins
        for i in range(2):
            for j in range(2):
                if state[i][j] != ' ' and state[i][j] == state[i+1][j + 1] == state[i+2][j + 2] == state[i+3][j + 3]:
                    return 1 if state[i][j]==self.my_piece else -1
                
        # check / diagonal wins
        for i in range(2):
            for j in range( 4, 2, -1):
                if state[i][j] != ' ' and state[i][j] == state[i+1][j - 1] == state[i+2][j - 2] == state[i+3][j - 3]:
                    return 1 if state[i][j]==self.my_piece else -1
                
        # check 2x2 box wins
        for i in range(4):
            for j in range(4):
                if state[i][j] != ' ' and state[i][j] == state[i + 1][j + 1] == state[i][j + 1] == state[i + 1][j]:
                    return 1 if state[i][j]==self.my_piece else -1
        
        return 0 # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################

def main():
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()

