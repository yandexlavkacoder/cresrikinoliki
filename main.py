import random
import os
from datetime import datetime

class TicTacGame:
    def __init__(self):
        self.players = ['X', 'O']
        self.current_turn = None
        self.mode = None
        self.stats_dir = "game_stats"
        self.create_stats_dir()
    
    def create_stats_dir(self):
        if not os.path.exists(self.stats_dir):
            os.makedirs(self.stats_dir)
    
    def save_game_result(self, result, board_size, moves_count):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{self.stats_dir}/game_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write(f"Game Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Board Size: {board_size}x{board_size}\n")
            f.write(f"Total Moves: {moves_count}\n")
            f.write(f"Game Result: {result}\n")
            f.write(f"Game Mode: {'Two Players' if self.mode == '1' else 'Player vs Computer'}\n")
    
    def make_board(self, n):
        board = []
        for i in range(n):
            row = []
            for j in range(n):
                row.append('-')
            board.append(row)
        return board
    
    def show_board(self, board):
        n = len(board)
        header = "  "
        for i in range(n):
            header += str(i+1) + " "
        print(header)
        
        for i in range(n):
            line = str(i+1) + " "
            for j in range(n):
                line += board[i][j] + " "
            print(line)
        print()
    
    def ask_board_size(self):
        while True:
            try:
                n = int(input("Board size (3-8): "))
                if 3 <= n <= 8:
                    return n
                print("Size must be between 3 and 8")
            except:
                print("Enter a valid number")
    
    def human_turn(self, board, mark):
        n = len(board)
        while True:
            try:
                move = input(f"Player {mark} move (row col): ")
                parts = move.split()
                if len(parts) != 2:
                    print("Enter two numbers")
                    continue
                    
                r, c = int(parts[0]), int(parts[1])
                
                if 1 <= r <= n and 1 <= c <= n:
                    if board[r-1][c-1] == '-':
                        return r-1, c-1
                    print("Cell taken")
                else:
                    print(f"Numbers 1-{n} only")
                    
            except:
                print("Invalid input")
    
    def computer_turn(self, board):
        n = len(board)
        free_cells = []
        
        for i in range(n):
            for j in range(n):
                if board[i][j] == '-':
                    free_cells.append((i, j))
        
        if free_cells:
            return random.choice(free_cells)
        return None, None
    
    def check_win(self, board, mark):
        n = len(board)
        
        for i in range(n):
            win_row = True
            for j in range(n):
                if board[i][j] != mark:
                    win_row = False
                    break
            if win_row:
                return True
        
        for j in range(n):
            win_col = True
            for i in range(n):
                if board[i][j] != mark:
                    win_col = False
                    break
            if win_col:
                return True
        
        win_diag1 = True
        for i in range(n):
            if board[i][i] != mark:
                win_diag1 = False
                break
        if win_diag1:
            return True
        
        win_diag2 = True
        for i in range(n):
            if board[i][n-1-i] != mark:
                win_diag2 = False
                break
        if win_diag2:
            return True
        
        return False
    
    def board_full(self, board):
        for row in board:
            if '-' in row:
                return False
        return True
    
    def select_mode(self):
        print("\nGame modes:")
        print("1 - Two players")
        print("2 - Vs computer")
        
        while True:
            choice = input("Select mode (1/2): ")
            if choice in ['1', '2']:
                return choice
            print("Enter 1 or 2")
    
    def pick_first(self):
        first = random.choice(['X', 'O'])
        print(f"{first} goes first")
        return first
    
    def play_round(self):
        self.mode = self.select_mode()
        
        size = self.ask_board_size()
        board = self.make_board(size)
        
        if self.mode == '1':
            self.current_turn = 'X'
        else:
            self.current_turn = self.pick_first()
        
        moves_count = 0
        
        while True:
            self.show_board(board)
            
            if self.mode == '2' and self.current_turn == 'O':
                print("Computer thinking...")
                r, c = self.computer_turn(board)
                if r is not None:
                    board[r][c] = 'O'
                    current_mark = 'O'
            else:
                r, c = self.human_turn(board, self.current_turn)
                board[r][c] = self.current_turn
                current_mark = self.current_turn
            
            moves_count += 1
            
            if self.check_win(board, current_mark):
                self.show_board(board)
                if self.mode == '2' and current_mark == 'O':
                    result = "Computer wins!"
                    print(result)
                else:
                    result = f"Player {current_mark} wins!"
                    print(result)
                self.save_game_result(result, size, moves_count)
                break
            
            if self.board_full(board):
                self.show_board(board)
                result = "It's a tie!"
                print(result)
                self.save_game_result(result, size, moves_count)
                break
            
            if self.mode == '1':
                self.current_turn = 'O' if self.current_turn == 'X' else 'X'
            else:
                self.current_turn = 'O' if self.current_turn == 'X' else 'X'
    
    def start_game(self):
        while True:
            self.play_round()
            
            while True:
                again = input("\nPlay again? (y/n): ").lower()
                if again in ['y', 'n']:
                    break
                print("Enter y or n")
            
            if again == 'n':
                print("Game over")
                break

if __name__ == "__main__":
    game = TicTacGame()
    game.start_game()