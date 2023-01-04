import random
import timeit
import time
import copy
import numpy as np

random.seed(time.time())

class Node_1:
    def __init__(self,
                 board: list,):
        self.board = copy.deepcopy(board)

class Node_2:
    def __init__(self,
                 board: list,
                 parent: 'Node_2' = None,):
        self.board = copy.deepcopy(board)
        self.parent = parent
        self.child = []
        self.win_simu = 0
        self.nums_simu = 0
        
    # functions used for MCTS
    def ratio(self):
        if self.nums_simu == 0:
            return 0
        return self.win_simu / self.nums_simu
          
class CoGanh:
    def __init__(self):
        # 2: Initial value, processing
        # 1: can move
        # 0: can't move
        self.moveBoard = []
        
    def getPosition(self, board, player):
        result = []
        for i in range(5):
            for j in range(5):
                if board[i][j] == player:
                    result.append((i, j))
        return result

    # If 0, the chessman at this position can move. Otherwise, it can't
    def cantMove(self, board, position):
        x, y = position[0], position[1]
        
        if self.moveBoard[x][y] == 0:
            return True
        elif self.moveBoard[x][y] == 1:
            return False
        
        # PART I
        if x > 0:
            if board[x - 1][y] == 0: 
                self.moveBoard[x][y] = 1
                return False
        if x < 4:
            if board[x + 1][y] == 0:
                self.moveBoard[x][y] = 1
                return False
        if y > 0:
            if board[x][y - 1] == 0:
                self.moveBoard[x][y] = 1
                return False
        if y < 4:
            if board[x][y + 1] == 0:
                self.moveBoard[x][y] = 1
                return False
        
        if (x + y) % 2 == 0:
            if x > 0 and y > 0:
                if board[x - 1][y - 1] == 0:
                    self.moveBoard[x][y] = 1
                    return False
            if x < 4 and y > 0:
                if board[x + 1][y - 1] == 0:
                    self.moveBoard[x][y] = 1
                    return False
            if x > 0 and y < 4:
                if board[x - 1][y + 1] == 0:
                    self.moveBoard[x][y] = 1
                    return False
            if x < 4 and y < 4:
                if board[x + 1][y + 1] == 0:
                    self.moveBoard[x][y] = 1
                    return 0
        
        # PART II
        player = board[x][y]
        board[x][y] = 2
        result = True
        
        if x > 0:
            if board[x - 1][y] == player:
                result = result and self.cantMove(board, (x - 1, y))
        if x < 4:
            if board[x + 1][y] == player:
                result = result and self.cantMove(board, (x + 1, y))
        if y > 0:
            if board[x][y - 1] == player:
                result = result and self.cantMove(board, (x, y - 1))
        if y < 4:
            if board[x][y + 1] == player:
                result = result and self.cantMove(board, (x, y + 1))
                
        if (x + y) % 2 == 0:
            if x > 0 and y > 0:
                if board[x - 1][y - 1] == player:
                    result = result and self.cantMove(board, (x - 1, y - 1))
            if x < 4 and y > 0:
                if board[x + 1][y - 1] == player:
                    result = result and self.cantMove(board, (x + 1, y - 1))
            if x > 0 and y < 4:
                if board[x - 1][y + 1] == player:
                    result = result and self.cantMove(board, (x - 1, y + 1))
            if x < 4 and y < 4:
                if board[x + 1][y + 1] == player:
                    result = result and self.cantMove(board, (x + 1, y + 1))
            
        if result:
            later = False
            if x > 0 and not later:
                if board[x - 1][y] == 2: later = True
            if x < 4 and not later:
                if board[x + 1][y] == 2: later = True
            if y > 0 and not later:
                if board[x][y - 1] == 2: later = True
            if y < 4 and not later:
                if board[x][y + 1] == 2: later = True
            if (x + y) % 2 == 0:
                if x > 0 and y > 0 and not later:
                    if board[x - 1][y - 1] == 2: later = True
                if x < 4 and y > 0 and not later:
                    if board[x + 1][y - 1] == 2: later = True
                if x > 0 and y < 4 and not later:
                    if board[x - 1][y + 1] == 2: later = True
                if x < 4 and y < 4 and not later:
                    if board[x + 1][y + 1] == 2: later = True
            
            if not later:
                self.moveBoard[x][y] = 0
        else:
            self.moveBoard[x][y] = 1
        
        return result
            
    def ganh(self, board, position, check = []):
        x, y = position[0], position[1]
        player = board[x][y]
        opponent = -1 * board[x][y]
        
        # HORIZONTAL
        if x > 0 and x < 4:
            if board[x - 1][y] == opponent and board[x + 1][y] == opponent:
                board[x - 1][y], board[x + 1][y] = player, player
                check.append(True)
        # VERTICAL
        if y > 0 and y < 4:
            if board[x][y - 1] == opponent and board[x][y + 1] == opponent:
                board[x][y - 1], board[x][y + 1] = player, player
                check.append(True)
        # DIAGONAL
        if ((x + y) % 2 == 0 and (x > 0 and x < 4) and (y > 0 and y < 4)):
            if board[x - 1][y - 1] == opponent and board[x + 1][y + 1] == opponent:
                board[x - 1][y - 1], board[x + 1][y + 1] = player, player
                check.append(True)
            if board[x - 1][y + 1] == opponent and board[x + 1][y - 1] == opponent:
                board[x - 1][y + 1], board[x + 1][y - 1] = player, player
                check.append(True)

    def chan(self, board, player):
        # Init moveBoard
        self.moveBoard = []
        for i in range(5):
            tmp = []
            for j in range(5):
                tmp.append(2)
            self.moveBoard.append(tmp)
        
        pos = self.getPosition(board, player)
        
        # Check which position is "chan"ed
        for p in pos:
            if self.cantMove(board, p):
                board[p[0]][p[1]] = -1 * player
                
            for i in range(5):
                for j in range(5):
                    if board[i][j] == 2:
                        board[i][j] = player
    
    # Return Node_1 and a position
    def move_gen(self, node: Node_1, position: tuple):
        x, y = position[0], position[1]
        player = node.board[x][y]
        opponent = -1 * player
        result = []
            
        # UP
        if x > 0:
            if node.board[x - 1][y] == 0:
                tmp_board = copy.deepcopy(node.board)
                tmp_board[x - 1][y] = copy.deepcopy(player)
                tmp_board[x][y] = 0
                
                # If len(check) > 0, then this move can "ganh"
                check = []
            
                self.ganh(tmp_board, (x - 1, y), check)
                self.chan(tmp_board, opponent)
                    
                tmp = Node_1(tmp_board)
                if len(check) > 0:
                    result.append((tmp, (x - 1, y), True, position))
                else:
                    result.append((tmp, (x - 1, y), False, position))
        # DOWN
        if x < 4:
            if node.board[x + 1][y] == 0:
                tmp_board = copy.deepcopy(node.board)
                tmp_board[x + 1][y] = copy.deepcopy(player)
                tmp_board[x][y] = 0
                
                # If len(check) > 0, then this move can "ganh"
                check = []
                
                self.ganh(tmp_board, (x + 1, y), check)
                self.chan(tmp_board, opponent)
                    
                tmp = Node_1(tmp_board)
                if len(check) > 0:
                    result.append((tmp, (x + 1, y), True, position))
                else:
                    result.append((tmp, (x + 1, y), False, position))
        # LEFT
        if y > 0:
            if node.board[x][y - 1] == 0:
                tmp_board = copy.deepcopy(node.board)
                tmp_board[x][y - 1] = copy.deepcopy(player)
                tmp_board[x][y] = 0
                
                # If len(check) > 0, then this move can "ganh"
                check = []
                
                self.ganh(tmp_board, (x, y - 1), check)
                self.chan(tmp_board, opponent)
                    
                tmp = Node_1(tmp_board)
                if len(check) > 0:
                    result.append((tmp, (x, y - 1), True, position))
                else:
                    result.append((tmp, (x, y - 1), False, position))
        # RIGHT
        if y < 4:
            if node.board[x][y + 1] == 0:
                tmp_board = copy.deepcopy(node.board)
                tmp_board[x][y + 1] = copy.deepcopy(player)
                tmp_board[x][y] = 0
                
                # If len(check) > 0, then this move can "ganh"
                check = []
                
                self.ganh(tmp_board, (x, y + 1), check)
                self.chan(tmp_board, opponent)
                    
                tmp = Node_1(tmp_board)
                if len(check) > 0:
                    result.append((tmp, (x, y + 1), True, position))
                else:
                    result.append((tmp, (x, y + 1), False, position))
                
        # DIAGONAL
        if (x + y) % 2 == 0:
            # UP LEFT
            if x > 0 and y > 0:
                if node.board[x - 1][y - 1] == 0:
                    tmp_board = copy.deepcopy(node.board)
                    tmp_board[x - 1][y - 1] = copy.deepcopy(player)
                    tmp_board[x][y] = 0
                    
                    # If len(check) > 0, then this move can "ganh"
                    check = []
                    
                    self.ganh(tmp_board, (x - 1, y - 1), check)
                    self.chan(tmp_board, opponent)
                        
                    tmp = Node_1(tmp_board)
                    if len(check) > 0:
                        result.append((tmp, (x - 1, y - 1), True, position))
                    else:
                        result.append((tmp, (x - 1, y - 1), False, position))
            # UP RIGHT
            if x > 0 and y < 4:
                if node.board[x - 1][y + 1] == 0:
                    tmp_board = copy.deepcopy(node.board)
                    tmp_board[x - 1][y + 1] = copy.deepcopy(player)
                    tmp_board[x][y] = 0
                    
                    # If len(check) > 0, then this move can "ganh"
                    check = []
                    
                    self.ganh(tmp_board, (x - 1, y + 1), check)
                    self.chan(tmp_board, opponent)
                        
                    tmp = Node_1(tmp_board)
                    if len(check) > 0:
                        result.append((tmp, (x - 1, y + 1), True, position))
                    else:
                        result.append((tmp, (x - 1, y + 1), False, position))
            # DOWN LEFT
            if x < 4 and y > 0:
                if node.board[x + 1][y - 1] == 0:
                    tmp_board = copy.deepcopy(node.board)
                    tmp_board[x + 1][y - 1] = copy.deepcopy(player)
                    tmp_board[x][y] = 0
                    
                    # If len(check) > 0, then this move can "ganh"
                    check = []
                    
                    self.ganh(tmp_board, (x + 1, y - 1), check)
                    self.chan(tmp_board, opponent)
                        
                    tmp = Node_1(tmp_board)
                    if len(check) > 0:
                        result.append((tmp, (x + 1, y - 1), True, position))
                    else:
                        result.append((tmp, (x + 1, y - 1), False, position))
            # DOWN RIGHT
            if x < 4 and y < 4:
                if node.board[x + 1][y + 1] == 0:
                    tmp_board = copy.deepcopy(node.board)
                    tmp_board[x + 1][y + 1] = copy.deepcopy(player)
                    tmp_board[x][y] = 0
                    
                    # If len(check) > 0, then this move can "ganh"
                    check = []
                    
                    self.ganh(tmp_board, (x + 1, y + 1), check)
                    self.chan(tmp_board, opponent)
                        
                    tmp = Node_1(tmp_board)
                    if len(check) > 0:
                        result.append((tmp, (x + 1, y + 1), True, position))
                    else:
                        result.append((tmp, (x + 1, y + 1), False, position))
                    
        return result
    
    # Using for MCTS
    # Return Node_2 and a position
    def move_gen_2(self, node: Node_2, position: tuple):
        x, y = position[0], position[1]
        player = node.board[x][y]
        opponent = -1 * player
        result = []
            
        # UP
        if x > 0:
            if node.board[x - 1][y] == 0:
                tmp_board = copy.deepcopy(node.board)
                tmp_board[x - 1][y] = copy.deepcopy(player)
                tmp_board[x][y] = 0
                
                # If len(check) > 0, then this move can "ganh"
                check = []
            
                self.ganh(tmp_board, (x - 1, y), check)
                self.chan(tmp_board, opponent)
                    
                tmp = Node_2(tmp_board, node)
                if len(check) > 0:
                    result.append((tmp, True))
                else:
                    result.append((tmp, False))
        # DOWN
        if x < 4:
            if node.board[x + 1][y] == 0:
                tmp_board = copy.deepcopy(node.board)
                tmp_board[x + 1][y] = copy.deepcopy(player)
                tmp_board[x][y] = 0
                
                # If len(check) > 0, then this move can "ganh"
                check = []
                
                self.ganh(tmp_board, (x + 1, y), check)
                self.chan(tmp_board, opponent)
                    
                tmp = Node_2(tmp_board, node)
                if len(check) > 0:
                    result.append((tmp, True))
                else:
                    result.append((tmp, False))
        # LEFT
        if y > 0:
            if node.board[x][y - 1] == 0:
                tmp_board = copy.deepcopy(node.board)
                tmp_board[x][y - 1] = copy.deepcopy(player)
                tmp_board[x][y] = 0
                
                # If len(check) > 0, then this move can "ganh"
                check = []
                
                self.ganh(tmp_board, (x, y - 1), check)
                self.chan(tmp_board, opponent)
                    
                tmp = Node_2(tmp_board, node)
                if len(check) > 0:
                    result.append((tmp, True))
                else:
                    result.append((tmp, False))
        # RIGHT
        if y < 4:
            if node.board[x][y + 1] == 0:
                tmp_board = copy.deepcopy(node.board)
                tmp_board[x][y + 1] = copy.deepcopy(player)
                tmp_board[x][y] = 0
                
                # If len(check) > 0, then this move can "ganh"
                check = []
                
                self.ganh(tmp_board, (x, y + 1), check)
                self.chan(tmp_board, opponent)
                    
                tmp = Node_2(tmp_board, node)
                if len(check) > 0:
                    result.append((tmp, True))
                else:
                    result.append((tmp, False))
                
        # DIAGONAL
        if (x + y) % 2 == 0:
            # UP LEFT
            if x > 0 and y > 0:
                if node.board[x - 1][y - 1] == 0:
                    tmp_board = copy.deepcopy(node.board)
                    tmp_board[x - 1][y - 1] = copy.deepcopy(player)
                    tmp_board[x][y] = 0
                    
                    # If len(check) > 0, then this move can "ganh"
                    check = []
                    
                    self.ganh(tmp_board, (x - 1, y - 1), check)
                    self.chan(tmp_board, opponent)
                        
                    tmp = Node_2(tmp_board, node)
                    if len(check) > 0:
                        result.append((tmp, True))
                    else:
                        result.append((tmp, False))
            # UP RIGHT
            if x > 0 and y < 4:
                if node.board[x - 1][y + 1] == 0:
                    tmp_board = copy.deepcopy(node.board)
                    tmp_board[x - 1][y + 1] = copy.deepcopy(player)
                    tmp_board[x][y] = 0
                    
                    # If len(check) > 0, then this move can "ganh"
                    check = []
                    
                    self.ganh(tmp_board, (x - 1, y + 1), check)
                    self.chan(tmp_board, opponent)
                        
                    tmp = Node_2(tmp_board, node)
                    if len(check) > 0:
                        result.append((tmp, True))
                    else:
                        result.append((tmp, False))
            # DOWN LEFT
            if x < 4 and y > 0:
                if node.board[x + 1][y - 1] == 0:
                    tmp_board = copy.deepcopy(node.board)
                    tmp_board[x + 1][y - 1] = copy.deepcopy(player)
                    tmp_board[x][y] = 0
                    
                    # If len(check) > 0, then this move can "ganh"
                    check = []
                    
                    self.ganh(tmp_board, (x + 1, y - 1), check)
                    self.chan(tmp_board, opponent)
                        
                    tmp = Node_2(tmp_board, node)
                    if len(check) > 0:
                        result.append((tmp, True))
                    else:
                        result.append((tmp, False))
            # DOWN RIGHT
            if x < 4 and y < 4:
                if node.board[x + 1][y + 1] == 0:
                    tmp_board = copy.deepcopy(node.board)
                    tmp_board[x + 1][y + 1] = copy.deepcopy(player)
                    tmp_board[x][y] = 0
                    
                    # If len(check) > 0, then this move can "ganh"
                    check = []
                    
                    self.ganh(tmp_board, (x + 1, y + 1), check)
                    self.chan(tmp_board, opponent)
                        
                    tmp = Node_2(tmp_board, node)
                    if len(check) > 0:
                        result.append((tmp, True))
                    else:
                        result.append((tmp, False))
                    
        return result

    def simple_move(self, board, start, end):
        x0, y0 = start[0], start[1]
        x1, y1 = end[0], end[1]
        
        # Check if it's a valid move
        valid = False
        if (
            x1 >= 0 and x1 < 5 and
            y1 >= 0 and y1 < 5 and
            (
                (x1 == x0 + 1 and y1 == y0) or
                (x1 == x0 - 1 and y1 == y0) or
                (x1 == x0 and y1 == y0 + 1) or
                (x1 == x0 and y1 == y0 -1) or
                ((x0 + y0) % 2 == 0 and
                    (x1 == x0 - 1 and y1 == y0 - 1) or
                    (x1 == x0 + 1 and y1 == y0 - 1) or
                    (x1 == x0 - 1 and y1 == y0 + 1) or
                    (x1 == x0 + 1 and y1 == y0 + 1)
                )
            )
        ):
            valid = True
        
        if not valid:
            print("Invalid move!!!")
            return
        
        board[x1][y1] = board[x0][y0]
        board[x0][y0] = 0
        
        self.ganh(board, end)
        self.chan(board, -1 * board[x1][y1])
        
    def back_prop(self, board1, board2, player):
        start, end = None, None
        
        for i in range(5):
            for j in range(5):
                if board1[i][j] == 0 and board2[i][j] == player:
                    end = (i, j)
                elif board1[i][j] == player and board2[i][j] == 0:
                    start = (i, j)
        
        return start, end
        
    def random_move(self, node, player):
        pos = self.getPosition(node.board, player)
        possible_moves = []
        
        for p in pos:
            possible_moves += self.move_gen_2(node, p)
        
        g = False
        for move in possible_moves:
            if move[1]:
                g = True
                break
        if g:
            possible_moves = [move for move in possible_moves if move[1]]
            
        rand = random.randint(0, len(possible_moves) - 1)
        return possible_moves[rand][0]
    
    def random_move_2(self, board, player):
        pos = self.getPosition(board, player)
        node = Node_1(board)
        successor = []
        for p in pos:
            successor += self.move_gen(node, p)
        
        g = False
        for s in successor:
            if s[2] == True:
                g = True
                break
            
        if g:
            successor = [move for move in successor if move[2]]
        
        rand = random.randint(0, len(successor) - 1)
        step = successor[rand]
        start, end = step[3], step[1]
        
        return (start, end)
                    
    def end_game(self, board, notice = True):
        score = sum(map(sum, board))
        if score == 16:
            if notice:
                print("\nX WIN!!!")
            return True
        elif score == -16:
            if notice:
                print("\nO WIN!!!")
            return True
        return False
    
    def X_win(self, board):
        score = sum(map(sum, board))
        if score == 16:
            return True
        return False
    
    def O_win(self, board):
        score = sum(map(sum, board))
        if score == -16:
            return True
        return False

class Solver:
    def __init__(self,
                 depth: int = 2,
                 board: list = None,
                 player: int = 1,):
        self.depth = depth
        self.board = copy.deepcopy(board)
        self.player, self.opponent = player, -1 * player
        
        self.start = None
        self.end = None
    
    def evaluate(self, board):
        return sum(map(sum, board))
    
    def play(self, node, dp):
        if dp > self.depth: 
            return
        
        # LEAF NODE
        if dp == self.depth:
            return self.evaluate(node.board)
        
        score = 0
        g = False
        cg = CoGanh()
        # PLAYER
        if dp % 2 == 0:
            score = -100
            successor = []
            pos = cg.getPosition(node.board, self.player)
                
            for p in pos:
                successor += cg.move_gen(node, p)
                
            if len(successor) > 0:
                for s in successor:
                    if s[2]:
                        g = True
                        break
                    
                for s in successor:
                    if g:
                        if not s[2]:
                            continue
                        
                    if cg.X_win(s[0].board):
                        if dp == 0:
                            self.start = s[3]
                            self.end = s[1]
                        return 100
                    
                    value = self.play(s[0], dp + 1)
                    if value > score:
                        score = value
                        if dp == 0:
                            self.start = s[3]
                            self.end = s[1]
        # OPPONENT
        else:
            score = 100
            successor = []
            pos = cg.getPosition(node.board, self.opponent)
                
            for p in pos:
                successor += cg.move_gen(node, p)
                
            if len(successor) > 0:
                for s in successor:
                    if s[2]:
                        g = True
                        break
                    
                for s in successor:
                    if g:
                        if not s[2]:
                            continue
                        
                    if cg.O_win(s[0].board): 
                        return -100
                    
                    value = self.play(s[0], dp + 1)
                    if value < score:
                        score = value
                        
        return score
    
    def solv(self):
        node = Node_1(self.board)
        score = self.play(node, 0)
        return (self.start, self.end)


def readBoard(file):
    count = 0
    board = []
    with open(file, 'r') as f:
        for line in f:
            board.append([int(x) for x in line.split()])
            count += 1
            if count == 5: break
    return board

def printBoard(board):
    for i in range(5):
        for j in range(5):
            e = ''
            if j == 4: e = '\n'
            if board[i][j] != -1:
                print(' ' + str(board[i][j]) + ' ', end = e)
            else:
                print(str(board[i][j]) + ' ', end = e)
    print('')

def writeBoardFile(board_be4_move, move: tuple, player):
    f = open("myboard.txt", "a")

    boardnp = np.array(board_be4_move) * player
    print(boardnp)

    for i in range(5):
        row = ''
        for j in range(5):
            e = ''
            if j == 4: e = '\n'
            if boardnp[i][j] != -1:
                row += ' ' + str(board_be4_move[i][j]) + ' '
            else:
                row += str(board_be4_move[i][j]) + ' '

        print(row)
        f.write(row + '\n')
    num = convert_move_2_num(move, map_num)
    f.write(str(num) + '\n')
    f.write('---- \n')
    
    
def saveBoard(board, file):
    with open(file, 'w') as f:
        for i in range(5):
            for j in range(5):
                if board[i][j] != -1:
                    f.write(' ' + str(board[i][j]) + ' ')
                else:
                    f.write(str(board[i][j]) + ' ')
            f.write('\n')
            
def nums(board, player):
    ans = 0
    for i in range(5):
        for j in range(5):
            if board[i][j] == player:
                ans += 1
    return ans


#co the viet them cac ham, bien khac

def move(prev_board, board, player, remain_time_x, remain_time_o): # khong sua ten ham nay
    start = timeit.default_timer()
    prev_board = copy.deepcopy(board)
    depth = 5
    solver = Solver(depth, board, player)
    result = solver.solv()
    
    stop = timeit.default_timer()
    
    time_step = stop - start
 
    if player == 1:
        remain_time_x -= time_step
    else:
        remain_time_o -= time_step
    
    
    return result, prev_board

def update_board_after_move(current_board: list, start_p: tuple, end_p: tuple, player: int):
    current_board[start_p[0]][start_p[1]] = 0
    current_board[end_p[0]][end_p[1]] = player

def mapping_move_2_num ():
    mapping = []
    for i in range(5):
        for j in range(5):
            pos = [(i-1,j-1),(i,j-1),(i+1,j-1),(i-1,j),(i+1,j),(i-1,j+1),(i,j+1),(i+1,j+1)]
            valid_pos = [((i,j),p) for p in pos if is_valid_pos(p) and correct_net_move((i,j),p)]
            
            mapping += valid_pos

    # print(mapping)
    return mapping

def convert_move_2_num (move: tuple, move_map_num: list):
    print("find move", move)
    try:
        return move_map_num.index(move)
        
    except:
        return -1


def is_valid_pos (pos: tuple):
    return pos[0] >= 0 and pos[0] < 5 and pos[1] >= 0 and pos[1] < 5

def correct_net_move(start, end):
    start_x, start_y = start
    end_x, end_y = end
    if (start_x + start_y) % 2 == 0:
        return True
    else:
        if abs(end_x - start_x) + abs(end_y-start_y) == 2:
            return False
        return True

def all_valid_move_of_player(player, cur_board, all_move):
    move_arr = []
    for tuple_move in all_move:
        start_pos, end_pos = tuple_move
        start_x, start_y = start_pos
        end_x, end_y = end_pos

        if cur_board[start_x][start_y] == player and cur_board[end_x][end_y] == 0:  
            move_arr.append(1)
            # print(start_pos, "move to", end_pos)
        else:
            move_arr.append(0)
    
    return move_arr

def generate_random_move (player_valid_move):
    move_index = range(0, len(player_valid_move))
    rdn = random.choices(move_index, weights=player_valid_move)
    print(">>> Random Generator", rdn[0])
    return rdn[0]

def ganh( board, position, check = []):
    x, y = position[0], position[1]
    player = board[x][y]
    opponent = -1 * board[x][y]
    
    # HORIZONTAL
    if x > 0 and x < 4:
        if board[x - 1][y] == opponent and board[x + 1][y] == opponent:
            board[x - 1][y], board[x + 1][y] = player, player
            check.append(True)
    # VERTICAL
    if y > 0 and y < 4:
        if board[x][y - 1] == opponent and board[x][y + 1] == opponent:
            board[x][y - 1], board[x][y + 1] = player, player
            check.append(True)
    # DIAGONAL
    if ((x + y) % 2 == 0 and (x > 0 and x < 4) and (y > 0 and y < 4)):
        if board[x - 1][y - 1] == opponent and board[x + 1][y + 1] == opponent:
            board[x - 1][y - 1], board[x + 1][y + 1] = player, player
            check.append(True)
        if board[x - 1][y + 1] == opponent and board[x + 1][y - 1] == opponent:
            board[x - 1][y + 1], board[x + 1][y - 1] = player, player
            check.append(True)

def chan(cur_board, player, map_move):
    # Init moveBoard
    player_pos = []
    for i in range(5):
        for j in range(5):
            if cur_board[i][j] == player:
                player_pos.append((i,j))
    
    visited = []
    for pos_tuple in player_pos:
        i, j = pos_tuple
        pos = [(i-1,j-1),(i,j-1),(i+1,j-1),(i-1,j),(i+1,j),(i-1,j+1),(i,j+1),(i+1,j+1)]
        valid_next_pos = [p for p in pos if is_valid_pos(p) and correct_net_move((i,j),p)]

        



### how to play
time_x = 1000000000
preboard = []
init_board = [[1, 1, 1, 1, 1],
 [1, 0, 0, 0, 1],
 [1, 0, 0, 0, -1],
 [-1, 0, 0, 0, -1],
 [-1, -1, -1, -1, -1]]
cur_player = 1
map_num = mapping_move_2_num()


for i in range(5):
    ## Monte Carlos player 1
    step, pre = move(preboard, init_board, cur_player,time_x, time_x)
    update_board_after_move(init_board, step[0], step[1], cur_player)
    print(">> Player 1")
    printBoard(init_board)
    convert_move_2_num(step, map_num)
    # writeBoardFile(pre, step, cur_player)

    ## Implement random for player 2
    second_player = -1
    player_valid = all_valid_move_of_player(second_player, init_board, map_num)
    random_move = generate_random_move(player_valid)
    cur_start, cur_end = map_num[random_move]
    print(cur_start, cur_end)
    update_board_after_move(init_board, cur_start, cur_end, second_player)
    print(">> Player 2")
    printBoard(init_board)
