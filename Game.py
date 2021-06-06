import chess
import chess.polyglot
import berserk
import threading
import json
from Minimax import Minimax
from evaluation import evaluation
from File import file

class Game(threading.Thread):
    def __init__(self, client, game_id, player_id, **kwargs):
        super().__init__(**kwargs)
        self.file = file()
        self.player_id = player_id
        self.game_id = game_id
        self.client = client
        self.stream = client.bots.stream_game_state(game_id)
        self.gameFull = None
        self.minimax = Minimax()
        self.color = ''
        self.numTurn = 1    # Num of Game Turn
        

        self.config = self.load_configuration()

        self.depth = self.config['depth']

    ################
    ### Main Run ###
    ################
    def run(self,training_file_name, training_file_path):
        """
        Possible values of Event Type:

        - [gameFull]  - Full game data. All values are immutable, except for the state field.
        - [gameState] - Current state of the game. Immutable values not included.
        - [chatLine]  - Chat message sent by a user (or the bot itself) in the room "player" or "spectator".

        """

        self.file.init_training(training_file_name, training_file_path)

        for event in self.stream:

            # Show new turn
            self.print_turn(event)

            if event['type'] == 'gameFull':
                # Starting Game & 1st move
                error_game = self.start_game_and_first_move(event)

                if error_game:
                    break    # Finish the game. There is some error

            elif event['type'] == 'gameState':
                # Next Move
                is_finished = self.next_move(event)

                if is_finished:
                    break    # Finish the game. We have a winner

            elif event['type'] == 'chatLine':
                # Incoming Chat Line
                self.handle_chat_line(event)

        # End Game
        self.file.close()
        self.print_endgame()


    ### Main 3 Acction Events ###
    def start_game_and_first_move(self, event):
        error_game = False

        # Init Game
        gameState = self.init_game_start(event)

        if gameState is None:
            # Some error is occurred with initial state
            error_game = True
        else:
            # Continue the game, next move
            self.play_next_move(gameState)

        return error_game

    def next_move(self, game_state):
        # Update current state into gameFull
        self.gameFull['state'] = game_state

        is_finish = False

        if 'winner' in game_state:
            # Game is finished
            self.print_winer(game_state)
            # Exit Game
            is_finish = True
        else:
            # Continue the game, next move
            self.play_next_move(game_state)

        return is_finish

    def handle_chat_line(self, chat_line):
        if chat_line['room'] == 'player':
            print(f" - Chat: [{chat_line['username']}]: {chat_line['text']}")
        elif chat_line['room'] == 'spectator':
            print(
                f" - Chat: [Spectator] [{chat_line['username']}]: {chat_line['text']}")

    
    ### Auxiliary methods ###
    def init_game_start(self, event):

        # Save gameFull
        self.gameFull = event
        gameState = gameState = self.gameFull['state']

        if 'id' in self.gameFull['white']:
            if self.gameFull['white']['id'] == self.player_id:
                # Playing with white
                self.color = 'white'
                self.print_player()

        elif 'id' in event['black']:
            if self.gameFull['black']['id'] == self.player_id:
                # playing with black
                self.color = 'black'
                self.print_player()
        else:
            # Error - User is neither Withe nor Black
            self.print_game_lauch_failed()
            gameState = None

        return gameState

    def play_next_move(self, game_state):

        # Get Board
        board = self.get_updated_board(game_state["moves"])

        # Save fen
        fen = board.fen()
        self.file.writeFen(fen)

        # Play move
        if self.is_my_turn(board):
            self.numTurn += 1
            # Generat a move
            move = self.get_move(board)
            # Send movement to server
            try:
                self.client.bots.make_move(self.game_id, move)
            except Exception as err:
                print('Error: ', err)

    def get_move(self, board):
        #Check if prenset in the opening book:
        try:            
            move = chess.polyglot.MemoryMappedReader("Perfect2021.bin").find(board).move
            return move
#
        except:
            move = self.minimax.minimax_play(self.depth, board, board.turn)
            return move

    def get_updated_board(self, moves):

        if not moves:
            # Init board
            board = chess.Board()
        else:
            # Retrieve moves from state
            board = self.get_pos_from_moves_list(moves)

        return board

    def get_pos_from_moves_list(self, moves):
        # convert the string of moves into a list that we can iterate
        moves_list = moves.split()
        # Starting from initial position, we  pushh all the moves to get the final state
        board = chess.Board()
        # Updating pborad with all the moves
        for move in moves_list:
            new_pos = chess.Move.from_uci(move)
            board.push(new_pos)
        return board

    def is_my_turn(self, board):

        if board.turn:
            turn = self.color == 'white'
        else:
            turn = self.color == 'black'

        return turn

    def victory_status(self, game_state):
        status = ''
        if game_state == self.color:
            status = 'WIN'
        else:
            status = 'LOSE'
        return status

    def load_configuration(self):

        json_file = open('config.json',)
        config = json.load(json_file)
        
        return config


    ## PRINTERS ##
    def print_winer(self, game_state):
        print(f"\nGood game!!! The Winner is: {game_state['winner']}\n")
        print('####################')
        print(f"##   YOU {self.victory_status(game_state['winner'])}     ##")
        print('####################')

    def print_player(self):
        print(f"\n ## Player: [{self.player_id}] plays with {self.color.upper()} ##\n\n")

    def print_game_lauch_failed(self):
            print(f'\n\n ## Game launch failed. Player [{self.player_id}] is neither White nor Black ##\n\n')

    def print_turn(self, event):
        print(f"  # Turn [{self.numTurn}] - Event_Type: {event['type']}\n")

    def print_endgame(self):
        print("\n------------------------------")
        print("          GAME END ")
        print("------------------------------\n")
