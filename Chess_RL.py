import json
import sys
from interface_lichess import lichess
from train import Training

def start_engine():

    config = load_configuration()

    connection = lichess(config['token'], config['train']['training_file_name'], config['train']['training_file_path'])

    if config['mode_game'].lower() == 'ai':
        game_ai(config['game']['num_games'], connection)

    elif config['mode_game'].lower() == 'train':
        train_ai(config['train']['training_file_name'], 
                 config['train']['training_file_path'],
                 config['train']['training_num_lines'], 
                 config['train']['num_trainings'], 
                 config['train']['training_iterations'],
                 config['weights']['weights_file_name'], 
                 config['weights']['weights_file_path'], 
                 connection)

    elif config['mode_game'].lower() == 'user':
        game_user(config['game']['num_games'], connection)

    else:
        print('Bad mode_game: Options: AI, User, Train')
        print('  - Edit config.json file and try again')


def load_configuration():

    json_file = open('config.json',)
    config = json.load(json_file)
    
    return config

def train_ai(training_file_name: str, training_file_path: str, training_num_lines: int, num_trainings: int, training_iterations: int, weights_file_name: str, weights_file_path: str, connection):
    for game_id in range(num_trainings):
        print_start_game(game_id)

        # 1 - Play Game (and generate Training sample Fens)
        connection.start_challenge_ai()
        connection.accept_challenge()
        
        # 2 - Init Training
        iteration=0
        while iteration < training_iterations :    
            train = Training(training_num_lines, training_file_name, weights_file_name, training_file_path, weights_file_path)
            train.run()
            iteration+=1


def game_ai(num_games, connection):
    for game_id in range(num_games):
        print_start_game(game_id)
        connection.start_challenge_ai()
        connection.accept_challenge()

def game_user(num_games, connection):
    for game_id in range(num_games):
        print_start_game(game_id)
        connection.accept_challenge()

def print_start_game(game_id):
    print("\n######################")
    print(f"    Start Game - {game_id + 1}")
    print("######################\n")


if __name__ == '__main__':
    start_engine()
