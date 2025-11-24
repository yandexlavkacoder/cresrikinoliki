import random

class TicTacToe:
    def __init__(self):
        self.player1 = 'X'
        self.player2 = 'O'
    
    def initialize_board(self, size):
        return [['.' for _ in range(size)] for _ in range(size)]
    
    def print_board(self, board):
        size = len(board)
        print("  " + " ".join(str(i+1) for i in range(size)))
        for i in range(size):
            print(f"{i+1} " + " ".join(board[i]))
        print()
    
    def get_valid_size(self):
        while True:
            try:
                size = int(input("Enter the size of the board (3-9): "))
                if 3 <= size <= 9:
                    return size
                else:
                    print("Invalid size, please enter again")
            except ValueError:
                print("Please enter a valid number")
    
    def get_valid_move(self, board, player):
        size = len(board)
        while True:
            try:
                move = input(f"{player}'s turn. Enter row and column (e.g. 1 2): ")
                row, col = map(int, move.split())
                
                if 1 <= row <= size and 1 <= col <= size:
                    if board[row-1][col-1] == '.':
                        return row-1, col-1
                    else:
                        print("This cell is already occupied. Choose another one.")
                else:
                    print(f"Please enter numbers between 1 and {size}")
            except ValueError:
                print("Please enter two numbers separated by space")
            except (IndexError, ValueError):
                print("Invalid input format. Please use: row column (e.g. 1 2)")
    
    def get_robot_move(self, board):
        size = len(board)
        empty_cells = []

        for i in range(size):
            for j in range(size):
                if board[i][j] == '.':
                    empty_cells.append((i, j))

        if empty_cells:
            return random.choice(empty_cells)
        return None
    
    def check_winner(self, board, player):
        size = len(board)
        
        
        for i in range(size):
            if all(board[i][j] == player for j in range(size)):
                return True

        for j in range(size):
            if all(board[i][j] == player for i in range(size)):
                return True
        
        if all(board[i][i] == player for i in range(size)):
            return True
        
        if all(board[i][size-1-i] == player for i in range(size)):
            return True
        
        return False
    
    def is_board_full(self, board):
        size = len(board)
        for i in range(size):
            for j in range(size):
                if board[i][j] == '.':
                    return False
        return True
    
    def choose_game_mode(self):
        """Выбор режима игры"""
        while True:
            print("\nChoose game mode:")
            print("1 - Player vs Player")
            print("2 - Player vs Robot")
            choice = input("Enter your choice (1 or 2): ")
            
            if choice in ['1', '2']:
                return choice
            else:
                print("Invalid choice. Please enter 1 or 2.")
    
    def choose_starting_player(self):
        return random.choice([self.player1, self.player2])
    
    def play_game(self):
        while True:
            print("\n=== Tic-Tac-Toe Game ===")
            
            game_mode = self.choose_game_mode()
            
            size = self.get_valid_size()
            board = self.initialize_board(size)
            
            current_player = self.choose_starting_player()
            print(f"\n{current_player} starts the game!")
            
            moves_count = 0
            
            while True:
                self.print_board(board)
                
                if game_mode == '2' and current_player == self.player2:
                    print("Robot's turn...")
                    row, col = self.get_robot_move(board)
                else:
                    row, col = self.get_valid_move(board, current_player)
                
                board[row][col] = current_player
                moves_count += 1
                
                if self.check_winner(board, current_player):
                    self.print_board(board)
                    result = f"{current_player} wins!"
                    print(result)
                    break
                
                if self.is_board_full(board):
                    self.print_board(board)
                    result = "Draw!"
                    print(result)
                    break
                
                current_player = self.player2 if current_player == self.player1 else self.player1
            
            while True:
                play_again = input("\nDo you want to play again? (y/n): ").lower()
                if play_again in ['y', 'n']:
                    break
                else:
                    print("Please enter 'y' for yes or 'n' for no")
            
            if play_again == 'n':
                print("Thanks for playing!")
                break

if __name__ == "__main__":
    game = TicTacToe()
    game.play_game()