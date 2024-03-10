import time


class TicTacToe:
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        
    def printBoard(self):
        print()
        print("--------------------------------")
        for row in self.board:
            print("|".join(row))
            print("-" * 5)
        print("--------------------------------")

    
    def checkWin(self, char):
        # Kiểm tra hàng và cột
        for i in range(3):
            if all(self.board[i][j] == char for j in range(3)):
                return True
            if all(self.board[j][i] == char for j in range(3)):
                return True
        # Kiểm tra đường chéo
        if all(self.board[i][i] == char for i in range(3)) or all(self.board[i][2 - i] == char for i in range(3)):
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
                if row not in range(3) or col not in range(3):
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
        bestScore = -100
        bestMove = (-1, -1)
        
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    self.board[i][j] = "O"
                    score = self.minimax(False)
                    
                    # What computer think
                    # self.printBoard()
                    # print(score)
                    # What computer think
                    
                    self.board[i][j] = " "
                    
                    if score > bestScore:
                        bestScore = score 
                        bestMove = (i, j)
        
        self.board[bestMove[0]][bestMove[1]] = "O"
        return
    
    def minimax(self, isMaximizing):
        if self.checkWin("O"):
            return 1
        elif self.checkWin("X"):
            return -1
        elif self.checkDraw():
            return 0
        
        if isMaximizing:
            bestScore = -100
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == " ":
                        self.board[i][j] = "O"
                        score = self.minimax(False)
                        self.board[i][j] = " "
                        
                        bestScore = max(bestScore, score)
            return bestScore
        else:
            bestScore = 100
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == " ":
                        self.board[i][j] = "X" 
                        score = self.minimax(True)
                        self.board[i][j] = " "
                        
                        bestScore = min(bestScore, score)
            return bestScore 
                        

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
