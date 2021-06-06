import random
import csv
import numpy
from numpy import genfromtxt




class file:

    

    def load_weights(self, file_name: str, path: str = None):
        
        path_full = self._get_file_path(file_name, path)
        weights=open(path_full, "r")
        
        W = genfromtxt(weights,delimiter=',')

        return W

    def save_weights(self, W, file_name: str, path: str = None):
        
        path_full = self._get_file_path(file_name, path)
        weights=open(path_full, "w")
        
        weights.truncate()
        numpy.savetxt(weights, W, delimiter = ",")
        weights.flush()
    


    def init_training(self, file_name: str, path: str = None):

        path_full = self._get_file_path(file_name, path)

        self.file = open(path_full, "w")

    def open_training(self, file_name: str, path: str = None):
        path_full = self._get_file_path(file_name, path)
        self.file = open(path_full, 'r')

    def read_list_of_fens(self):
        return self.file.readlines()

    
    def read_n_lines(self, num_lines):
        lines = self.read_list_of_fens()
        max_line = len(lines) - num_lines
        
        first_line = random.randint(0, max_line)
        last_line = first_line + num_lines

        return lines[first_line:last_line]

    def writeFen(self, fen: str):
        self.file.write(fen + "\n")
        self.file.flush()
        # print('Write Fen to file: ', fen)

    def close(self):
        self.file.close()

    def _get_file_path(self, file_name: str, path: str = None) -> str:
        if path is None or path == "":
            path_full = file_name
        else:
            path_full = path + "'\'" + file_name
        return path_full
