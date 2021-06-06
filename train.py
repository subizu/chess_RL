### Load Weights
### Call Game
### Load training_set
### Create n training_samples [5 boards FENS]
### Convert trainning_sample from FEN to BOARD
### For each n trainning_sample, call TDleaf.XXXXX
### Save wiehgts

import json
import chess
from File import file
from TDleaf import TDleaf
from evaluation import evaluation
import numpy as np


class Training:
    def __init__(self, training_num_lines: int, training_file_name: str, weights_file_name: str, training_path: str = None, weights_path: str = None
                , alpha = 0.5, gamma = 1, lmda = 0.7):
        self.num_lines = training_num_lines
        self.training_file_name = training_file_name
        self.training_path = training_path
        self.weights_file_name = training_file_name
        self.weights_path = training_path

        self.alpha = alpha
        self.gamma = gamma
        self.lmda = lmda
        

        self.td_leaf = TDleaf()
        self.evaluation = evaluation()
        self.config = self.load_configuration()

        self.depth = self.config['depth']



    def run(self):
        training_samples_fen = self.load_training_set_fen()
        W = self.load_weights()

        training_samples =[]             
        for fen in training_samples_fen:
            board = chess.Board(fen)
            training_samples.append(board)
        
        #Calculate the total pieces of the first board in training_samples to determine the wirghts to be trainied.
        total_pieces = self.evaluation.get_number_of_pieces(training_samples[0])
        w= W[total_pieces-1]
            
        W[total_pieces-1] = (self.td_leaf.tdleaf(training_samples, self.alpha, self.gamma, self.lmda, w, self.depth)) 

        #Normalize weights to sum 1
        W[total_pieces-1] = W[total_pieces-1] / W[total_pieces-1].min()
        W[total_pieces-1] = W[total_pieces-1] / np.sum(W[total_pieces-1] )
        

        self.save_weights(W)


        ##return W_updated


        
    
    def load_training_set_fen(self):
        f = file()
        f.open_training(self.training_file_name, self.training_path)
        return f.read_n_lines(self.num_lines)

    def load_weights(self):
        config=self.load_configuration() 
        weights =file()
        W = weights.load_weights(config['weights']['weights_file_name'], config['weights']['weights_file_path'])
        
        return W

    def save_weights(self, W_updated):
        config=self.load_configuration() 
        weights =file()
        weights.save_weights(W_updated,config['weights']['weights_file_name'], config['weights']['weights_file_path'])

    def load_configuration(self):

        json_file = open('config.json',)
        config = json.load(json_file)
        
        return config

