import time

# Player: X
# Computer: O


class TicTacToe:
    def __init__(self):
        self.board = [[" " for _ in range(5)] for _ in range(5)]
        self.winning_length = 4
        self.limit_search_time = 5
        self.limit_search_depth = 4


    def printBoard(self):
        print("--------------------------------")
        for row in self.board:
            print("|".join(row))
            print("-" * 9)
        print("--------------------------------")

    
    def checkWin(self, char):
        # Kiểm tra hàng
        for i in range(len(self.board)):
            for j in range(len(self.board) - self.winning_length + 1):
                if all(self.board[i][j+k] == char for k in range(self.winning_length)):
                    return True
        # Kiểm tra cột
        for i in range(len(self.board) - self.winning_length + 1):
            for j in range(len(self.board)):
                if all(self.board[i+k][j] == char for k in range(self.winning_length)):
                    return True
        # Kiểm tra đường chéo chính
        for i in range(len(self.board) - self.winning_length + 1):
            for j in range(len(self.board) - self.winning_length + 1):
                if all(self.board[i+k][j+k] == char for k in range(self.winning_length)):
                    return True
        # Kiểm tra đường chéo phụ
        for i in range(len(self.board) - self.winning_length + 1):
            for j in range(self.winning_length - 1, len(self.board)):
                if all(self.board[i+k][j-k] == char for k in range(self.winning_length)):
                    return True
        return False
    
    def checkDraw(self):
        for row in self.board:
            for cell in row:
                if cell == " ":
                    return False
        return True
    
    def playerMove(self):
        while True:
            try:
                row, col = list(map(int, input(f"Please enter row number (0-2) and col number (0-2): ").split()))
                if row not in range(5) or col not in range(5):
                    print("Invalid input! Please enter row and column numbers between 0 and 2.")
                    continue
            except ValueError:
                print("Invalid input! Please enter two numbers separated by a space.")
                continue
            
            if self.board[row][col] == " ":
                self.board[row][col] = "X"
                return
            else:
                print("This cell is already filled. Please choose another one.")


    def computerMove(self):
        # Step 1: Check if there is a move that wins immediately
        canWinIn1Move = self.winIn1Move("O")
        if canWinIn1Move:
            self.board[canWinIn1Move[0]][canWinIn1Move[1]] = "O"
            return
        
        # Step 2: Check if there is a move that causes the opponent to win immediately
        canLoseIn1Move = self.winIn1Move("X")
        if canLoseIn1Move: 
            self.board[canLoseIn1Move[0]][canLoseIn1Move[1]] = "O"
            return         
        
        # Step 3: Check if there is a fork opportunity: -OO--, --OO-, or -O-O- . If so, it ensures a win in 2 moves by transforming it into -OOO-
        canWinByFork = self.winByFork("O")
        if canWinByFork:
            self.board[canWinByFork[0]][canWinByFork[1]] = "O"
            return
        
        # Step 4: Check if there is a fork opportunity: -XX--, --XX-, or -X-X- . If so, it ensures not to lose in 2 moves by transforming it into -XXX-
        canLoseByFork = self.winByFork("X")
        if canLoseByFork:
            self.board[canLoseByFork[0]][canLoseByFork[1]] = "O"
            return
        
        bestScore = -10**9
        bestMove = (-1, -1)
        
        print("I WILL START!")
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == " ":
                    self.board[i][j] = "O"
                    score = self.minimax(False, 0)
                    
                    self.printBoard()
                    print("\033[91mScore for this board\033[0m", score)
                    
                    self.board[i][j] = " "
                    
                    if score > bestScore:
                        bestScore = score 
                        bestMove = (i, j)
        
        self.board[bestMove[0]][bestMove[1]] = "O"
        print("I 'M DONE!")
        return
    
    def minimax(self, isMaximizing, depth):
        if depth == self.limit_search_depth or self.checkDraw():
            return self.evaluate()
        
        
        if isMaximizing:
            bestScore = -10**9
            for i in range(5):
                for j in range(5):
                    if self.board[i][j] == " ":
                        self.board[i][j] = "O"
                        score = self.minimax(False, depth + 1)

                        
                        # self.printBoard()
                        # print("\033[91mDepth, Score\033[0m", depth, score)
                        # temp = input()

                        self.board[i][j] = " "
                        bestScore = max(bestScore, score)
            return bestScore
        else:
            bestScore = 10**9
            for i in range(5):
                for j in range(5):
                    if self.board[i][j] == " ":
                        self.board[i][j] = "X" 
                        score = self.minimax(True, depth + 1)

                        
                        # self.printBoard()
                        # print("\033[91mDepth, Score\033[0m", depth, score)
                        # temp = input()

                        self.board[i][j] = " "
                        bestScore = min(bestScore, score)
            return bestScore 
                        
    def winIn1Move(self, char):
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == " ":
                    self.board[i][j] = char
                    if self.checkWin(char):
                        self.board[i][j] = " "
                        return (i, j)
                    self.board[i][j] = " "
        return False


    
    def winByFork(self, char):
        # Check row
        for i in range(5):
            if self.board[i] == [" ", char, char, " ", " "]:
                return (i, 3)
            if self.board[i] == [" ", " ", char, char, " "]:
                return (i, 1)
            if self.board[i] == [" ", char, " ", char, " "]:
                return (i, 2)

        # Check column
        for j in range(5):
            column = [self.board[i][j] for i in range(5)]
            if column == [" ", char, char, " ", " "]:
                return (3, j)
            if column == [" ", " ", char, char, " "]:
                return (1, j)
            if column == [" ", char, " ", char, " "]:
                return (2, j)

        # Check main diagonal (\)
        main_diagonal = [self.board[i][i] for i in range(5)]
        if main_diagonal == [" ", char, char, " ", " "]:
            return (3, 3)
        if main_diagonal == [" ", " ", char, char, " "]:
            return (1, 1)
        if main_diagonal == [" ", char, " ", char, " "]:
            return (2, 2)

        # Check anti-diagonal (/)
        anti_diagonal = [self.board[i][4 - i] for i in range(5)]
        if anti_diagonal == [" ", char, char, " ", " "]:
            return (3, 1)
        if anti_diagonal == [" ", " ", char, char, " "]:
            return (1, 3)
        if anti_diagonal == [" ", char, " ", char, " "]:
            return (2, 2)

        return False
    
    def evaluate(self):
        score = 0
        
        # If computer can win immediately
        if self.checkWin("O"):
            score += 10**5
        # If opponent can win immediately
        elif self.checkWin("X"):
            score -= 10**5
        
        # If computer has 3-O in a row (1 more move to win)
        for i in range(5):
            for j in range(3):
                if self.board[i][j] == self.board[i][j+1] == self.board[i][j+2] == "O" and (j == 0 or self.board[i][j-1] != "O") and (j+2 == 4 or self.board[i][j+3] != "O"):
                    score += 10**4
                elif self.board[i][j] == self.board[i][j+1] == self.board[i][j+2] == "X" and (j == 0 or self.board[i][j-1] != "X") and (j+2 == 4 or self.board[i][j+3] != "X"):
                    score -= 10**4
            
        for j in range(5):
            for i in range(3):
                if self.board[i][j] == self.board[i+1][j] == self.board[i+2][j] == "O" and (i == 0 or self.board[i-1][j] != "O") and (i+2 == 4 or self.board[i+3][j] != "O"):
                    score += 10**4
                elif self.board[i][j] == self.board[i+1][j] == self.board[i+2][j] == "X" and (i == 0 or self.board[i-1][j] != "X") and (i+2 == 4 or self.board[i+3][j] != "X"):
                    score -= 10**4
        
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == self.board[i+1][j+1] == self.board[i+2][j+2] == "O" and (i == 0 or j == 0 or self.board[i-1][j-1] != "O") and (i+2 == 4 or j+2 == 4 or self.board[i+3][j+3] != "O"):
                    score += 10**4
                elif self.board[i][j] == self.board[i+1][j+1] == self.board[i+2][j+2] == "X" and (i == 0 or j == 0 or self.board[i-1][j-1] != "X") and (i+2 == 4 or j+2 == 4 or self.board[i+3][j+3] != "X"):
                    score -= 10**4
        
        for i in range(3):
            for j in range(2, 5):
                if self.board[i][j] == self.board[i+1][j-1] == self.board[i+2][j-2] == "O" and (i == 0 or j == 4 or self.board[i-1][j+1] != "O") and (i+2 == 4 or j-2 == 0 or self.board[i+3][j-3] != "O"):
                    score += 10**4
                elif self.board[i][j] == self.board[i+1][j-1] == self.board[i+2][j-2] == "X" and (i == 0 or j == 4 or self.board[i-1][j+1] != "X") and (i+2 == 4 or j-2 == 0 or self.board[i+3][j-3] != "X"):
                    score -= 10**4

        # if computer has fork (2 more move to win)
        for i in range(5):
            for j in range(3):
                if self.board[i][j] == self.board[i][j+1] == self.board[i][j+2] == "O" and (j == 0 or self.board[i][j-1] != "O") and (j+2 == 4 or self.board[i][j+3] != "O"):
                    score += 10**3
                elif self.board[i][j] == self.board[i][j+1] == self.board[i][j+2] == "X" and (j == 0 or self.board[i][j-1] != "X") and (j+2 == 4 or self.board[i][j+3] != "X"):
                    score -= 10**3
            
        for j in range(5):
            for i in range(3):
                if self.board[i][j] == self.board[i+1][j] == self.board[i+2][j] == "O" and (i == 0 or self.board[i-1][j] != "O") and (i+2 == 4 or self.board[i+3][j] != "O"):
                    score += 10**3
                elif self.board[i][j] == self.board[i+1][j] == self.board[i+2][j] == "X" and (i == 0 or self.board[i-1][j] != "X") and (i+2 == 4 or self.board[i+3][j] != "X"):
                    score -= 10**3
        
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == self.board[i+1][j+1] == self.board[i+2][j+2] == "O" and (i == 0 or j == 0 or self.board[i-1][j-1] != "O") and (i+2 == 4 or j+2 == 4 or self.board[i+3][j+3] != "O"):
                    score += 10**3
                elif self.board[i][j] == self.board[i+1][j+1] == self.board[i+2][j+2] == "X" and (i == 0 or j == 0 or self.board[i-1][j-1] != "X") and (i+2 == 4 or j+2 == 4 or self.board[i+3][j+3] != "X"):
                    score -= 10**3
        
        for i in range(3):
            for j in range(2, 5):
                if self.board[i][j] == self.board[i+1][j-1] == self.board[i+2][j-2] == "O" and (i == 0 or j == 4 or self.board[i-1][j+1] != "O") and (i+2 == 4 or j-2 == 0 or self.board[i+3][j-3] != "O"):
                    score += 10**3
                elif self.board[i][j] == self.board[i+1][j-1] == self.board[i+2][j-2] == "X" and (i == 0 or j == 4 or self.board[i-1][j+1] != "X") and (i+2 == 4 or j-2 == 0 or self.board[i+3][j-3] != "X"):
                    score -= 10**3

        # if computer has 2-O in a row 
        for i in range(5):
            for j in range(4):
                if self.board[i][j] == self.board[i][j+1] == "O" and (j == 0 or self.board[i][j-1] != "O") and (j+1 == 4 or self.board[i][j+2] != "O"):
                    score += 10**2
                elif self.board[i][j] == self.board[i][j+1] == "X" and (j == 0 or self.board[i][j-1] != "X") and (j+1 == 4 or self.board[i][j+2] != "X"):
                    score -= 10**2
        
        for j in range(5):
            for i in range(4):
                if self.board[i][j] == self.board[i+1][j] == "O" and (i == 0 or self.board[i-1][j] != "O") and (i+1 == 4 or self.board[i+2][j] != "O"):
                    score += 10**2
                elif self.board[i][j] == self.board[i+1][j] == "X" and (i == 0 or self.board[i-1][j] != "X") and (i+1 == 4 or self.board[i+2][j] != "X"):
                    score -= 10**2
        
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == self.board[i+1][j+1] == "O" and (i == 0 or j == 0 or self.board[i-1][j-1] != "O") and (i+1 == 4 or j+1 == 4 or self.board[i+2][j+2] != "O"):
                    score += 10**2
                elif self.board[i][j] == self.board[i+1][j+1] == "X" and (i == 0 or j == 0 or self.board[i-1][j-1] != "X") and (i+1 == 4 or j+1 == 4 or self.board[i+2][j+2] != "X"):
                    score -= 10**2
        
        for i in range(4):
            for j in range(1, 5):
                if self.board[i][j] == self.board[i+1][j-1] == "O" and (i == 0 or j == 4 or self.board[i-1][j+1] != "O") and (i+1 == 4 or j-1 == 0 or self.board[i+2][j-2] != "O"):
                    score += 10**2
                elif self.board[i][j] == self.board[i+1][j-1] == "X" and (i == 0 or j == 4 or self.board[i-1][j+1] != "X") and (i+1 == 4 or j-1 == 0 or self.board[i+2][j-2] != "X"):
                    score -= 10**2

        # Score += 10 for each O
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == "O":
                    score += 10
                elif self.board[i][j] == "X":
                    score -= 10
        
        return score

        
    def play(self):
        while True:
            self.printBoard()
            self.playerMove()
            
            if self.checkWin('X'):
                self.printBoard()
                print("You win!")
                break
            elif self.checkDraw():
                self.printBoard()
                print("It's a draw!")
                break
            
            start_time = time.time()
            self.computerMove()
            end_time = time.time()
            print("\033[91mComputer thinking time:\033[0m", end_time - start_time)
            
            if self.checkWin('O'):
                self.printBoard()
                print("Computer win!")
                break
            elif self.checkDraw():
                self.printBoard()
                print("It's a draw!")
                break

game = TicTacToe()
game.play()
