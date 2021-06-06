
import chess
import berserk
from Game import Game


class lichess():
    def __init__(self, token:str, training_file_name: str, training_file_path: str):
        # BERSEK API
        self.token = token
        self.training_file_name = training_file_name
        self.training_file_path = training_file_path

        # Authentication
        session = berserk.TokenSession(self.token)
        self.client = berserk.Client(session)
        

    def start_challenge_ai(self):
        self.client.challenges.create_ai(level=2, color = 'white')

    def accept_challenge(self):  # Accept challenge
        is_polite = True

        """
        Possible values of Event Type:

        - [gameStart]         - Start of a game
        - [gameFinish]        - Completion of a game
        - [challenge]         - A player sends you a challenge
        - [challengeCanceled] - A player cancels their challenge to you
        - [challengeDeclined] - The opponent declines your challenge
        """

        for event in self.client.bots.stream_incoming_events():
            # print(event)

            if event['type'] == 'gameStart':
                player_id = self.client.account.get()['username']
                game = Game(self.client, event['game']['id'], player_id)
                game.run(self.training_file_name, self.training_file_path)
                break

            elif event['type'] == 'challenge':
                if self.should_accept(event):
                    self.client.bots.accept_challenge(event['challenge']['id'])
                elif is_polite:
                    self.client.bots.decline_challenge(
                        event['challenge']['id'])

            elif event['type'] == 'gameFinish':
                print('Event Type: gameFinish')
                break

            elif event['type'] == 'challengeCanceled':
                print('Event Type: challengeCanceled')
                break

            elif event['type'] == 'challengeDeclined':
                print('Event Type: challengeDeclined')
                break

    def create_challenge(self):
        pass

    def should_accept(self, event):
        # if event['challenge']:
        return True
