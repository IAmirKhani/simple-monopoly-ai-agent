from copy import deepcopy
from property import *
from player import *

# Define the Monopoly game class
class MonopolyGame:
    def __init__(self, board=[], players=[], current_player=0, game_over=False):
        # Initialize the game state
        self.board = board  # List to represent the game board
        self.players = players  # List to represent the players
        self.current_player = current_player  # Index of the current player in the players list
        self.game_over = game_over  # Boolean flag to indicate if the game is over
    
    def initialize_board(self, file_name):
        # Initialize the game board from a csv file
        with open(file_name) as file:
            next(file)
            for line in file:
                name, space, color, position, price, build_price, rent = line.rstrip().split(",")
                self.board.append(
                    Property(name, space, color, int(position), int(price), int(rent), int(build_price))
                    )
        
        

    def initialize_players(self):
        # Initialize the players with their starting positions, money, and other attributes
        # Example: Create two players with initial attributes
        player1 = Player("P1", 0, 1500)
        player2 = Player("P2", 0, 1500)
        self.players = [player1, player2]

    def make_move(self, action):
        # Update the game state based on the action taken by the current player
        new_players = deepcopy(self.players)
        new_board = deepcopy(self.board)
        curr_player = new_players[self.current_player]
        curr_position = curr_player.position
        curr_prop = new_board[curr_position]
        if action is 0:
            pass
        elif action is 1:
            curr_player.money -= curr_prop.price
            curr_player.properties.append(curr_position)
            curr_prop.owner = self.current_player    
        elif action is 2:
            curr_player.money -= curr_prop.rent
            new_players[curr_prop.owner].money += curr_prop.rent
        
        return MonopolyGame(new_board, new_players, self.current_player, self.game_over)
    
    def get_possible_moves(self):
        # Get the possible moves available to the current player
        curr_player = self.players[self.current_player]
        curr_position = curr_player.position
        curr_prop = self.board[curr_position]
        if curr_prop.ownable:
            if curr_prop.owner == self.current_player:
                return [3, 4]
            elif curr_prop.owner == None:
                if curr_player.money > curr_prop.price:
                    return [1, 0]
                return [0]
            else:
                return [2]
        return [0]
    
    def move_player(self, dice_result):
        curr_player = self.players[self.current_player]
        curr_position = curr_player.position
        # Update the player's position based on the dice roll result
        curr_position = (curr_position + dice_result) % len(self.board)
        curr_player.position = curr_position

    def is_terminal(self):
        # Check if the game has reached a terminal state
        curr_player = self.players[self.current_player]
        if curr_player.money <= 0:
            return True
        return False
    
    def evaluate_utility(self):
        curr_player = self.players[self.current_player]
        # Evaluate the utility of the current game state for the current player
        return curr_player.net_worth(self.board)

    def switch_player(self):
        # Switch to the next player's turn
        self.current_player += 1
        self.current_player %= 2

