import json
import chess
from File import file

class evaluation():
    def __init__(self):

        # Piece Values in centipawns
        self.pawn = 1
        self.knight = 3
        self.bishop = 3
        self.rook = 5
        self.queen = 9
        self.king = 25

        
        #load weights
        
        self.config=self.load_configuration() 
        self.weights =file()
        self.W = self.weights.load_weights(self.config['weights']['weights_file_name'], self.config['weights']['weights_file_path'])
        
        

    
    
    def get_evaluation(self, board):

        if board.is_checkmate():
            if board.turn:
                return 999
            else:
                return -999
        elif board.is_stalemate():
            return 0
        elif board.is_insufficient_material():
            return 0
        else:

            material, development, mobility, control, tension, safety = self.get_features_eval(board)
            board_pieces = self.get_number_of_pieces(board)

            w = self.W[board_pieces-1]
            
            w1 = w[0]
            w2 = w[1]
            w3 = w[2]
            w4 = w[3]
            w5 = w[4]
            w6 = w[5]
            

            return w1*material + w2*development + w3*mobility + w4*control + w5*tension + w6*safety



    def get_features_eval(self, board):
        
        material = self.get_eval_material(board)
        development = self.get_eval_developement(board)
        mobility = self.get_eval_mobility(board)
        control = self.get_eval_control(board)
        tension = self.get_eval_tension(board)
        safety = self.get_eval_Ksafety(board)

        return [material, development, mobility, control, tension, safety]

    def get_eval_material(self, board):

        """
        Based on Matthew P. Tedesco, Ph.D. mptedesco @ https://github.com/mptedesco/python-chess-analysis.git 
        """
        # Material
        whitepawns = len(board.pieces(1,1))
        whiteknights = len(board.pieces(2,1))
        whitebishops = len(board.pieces(3,1))
        whiterooks = len(board.pieces(4,1))
        whitequeens = len(board.pieces(5,1))
        whiteking = len(board.pieces(6,1))
        whitematerial = self.pawn*whitepawns + self.knight*whiteknights + self.bishop*whitebishops + \
                        self.rook*whiterooks + self.queen*whitequeens +self.king*whiteking
        blackpawns = len(board.pieces(1,0))
        blackknights = len(board.pieces(2,0))
        blackbishops = len(board.pieces(3,0))
        blackrooks = len(board.pieces(4,0))
        blackqueens = len(board.pieces(5,0))
        blackking = len(board.pieces(6,0))
        blackmaterial = self.pawn*blackpawns + self.knight*blackknights + self.bishop*blackbishops + \
                        self.rook*blackrooks + self.queen*blackqueens +self.king*blackking
        material = whitematerial - blackmaterial

        return material

    def get_eval_developement(self, board):
            # Development - number of pieces no longer on starting squares for both sides
            # We give priority to the minor pieces before developing Q, R or K.
            whitedevelopment = 25
            blackdevelopment = 25
            if board.piece_at(chess.square(0,0)):
                if board.piece_at(chess.square(0,0)).symbol() == "R":
                    whitedevelopment -= 2
            if board.piece_at(chess.square(1,0)):
                if board.piece_at(chess.square(1,0)).symbol() == "N":
                    whitedevelopment -= 3
            if board.piece_at(chess.square(2,0)):
                if board.piece_at(chess.square(2,0)).symbol() == "B":
                    whitedevelopment -= 3
            if board.piece_at(chess.square(3,0)):
                if board.piece_at(chess.square(3,0)).symbol() == "Q":
                    whitedevelopment -= 2
            if board.piece_at(chess.square(4,0)):
                if board.piece_at(chess.square(4,0)).symbol() == "K":
                    whitedevelopment -= 1
            if board.piece_at(chess.square(5,0)):
                if board.piece_at(chess.square(5,0)).symbol() == "B":
                    whitedevelopment -= 3
            if board.piece_at(chess.square(6,0)):
                if board.piece_at(chess.square(6,0)).symbol() == "N":
                    whitedevelopment -= 3
            if board.piece_at(chess.square(7,0)):
                if board.piece_at(chess.square(7,0)).symbol() == "R":
                    whitedevelopment -= 2
            if board.piece_at(chess.square(3,1)):
                if board.piece_at(chess.square(3,1)).symbol() == "P":
                    whitedevelopment -= 3
            if board.piece_at(chess.square(4,1)):
                if board.piece_at(chess.square(4,1)).symbol() == "P":
                    whitedevelopment -= 3
            if board.piece_at(chess.square(0,7)):
                if board.piece_at(chess.square(0,7)).symbol() == "r":
                    blackdevelopment -= 2
            if board.piece_at(chess.square(1,7)):
                if board.piece_at(chess.square(1,7)).symbol() == "n":
                    blackdevelopment -= 3
            if board.piece_at(chess.square(2,7)):
                if board.piece_at(chess.square(2,7)).symbol() == "b":
                    blackdevelopment -= 3
            if board.piece_at(chess.square(3,7)):
                if board.piece_at(chess.square(3,7)).symbol() == "q":
                    blackdevelopment -= 2
            if board.piece_at(chess.square(4,7)):
                if board.piece_at(chess.square(4,7)).symbol() == "k":
                    blackdevelopment -= 1
            if board.piece_at(chess.square(5,7)):
                if board.piece_at(chess.square(5,7)).symbol() == "b":
                    blackdevelopment -= 3
            if board.piece_at(chess.square(6,7)):
                if board.piece_at(chess.square(6,7)).symbol() == "n":
                    blackdevelopment -= 3
            if board.piece_at(chess.square(7,7)):
                if board.piece_at(chess.square(7,7)).symbol() == "r":
                    blackdevelopment -= 2
            if board.piece_at(chess.square(3,6)):
                if board.piece_at(chess.square(3,6)).symbol() == "p":
                    blackdevelopment -= 3
            if board.piece_at(chess.square(4,6)):
                if board.piece_at(chess.square(4,6)).symbol() == "p":
                    blackdevelopment -= 3
            
            development = whitedevelopment - blackdevelopment 


            return development
        


    def get_eval_mobility(self, board):
        
        """
        Based on Matthew P. Tedesco, Ph.D. mptedesco @ https://github.com/mptedesco/python-chess-analysis.git 
        """
        # Mobility
        # Calculate all legal moves for white and black
        mobility1 = len(list(board.generate_legal_moves()))
        # Change side to move by pushing a null move and calculate all moves for opponent
        board.push(chess.Move.null())
        mobility2 = len(list(board.generate_legal_moves()))
        # Take back the null move to reset the board back to the position
        board.pop()
        if board.turn:
            mobility = mobility2 - mobility1
        else:
            mobility = mobility1 - mobility2
        
        return mobility

    def get_eval_control(self, board):            
        
        """
        Based on Matthew P. Tedesco, Ph.D. mptedesco @ https://github.com/mptedesco/python-chess-analysis.git 
        """
        # Control
        # Control is closely associated with "Space"
        # We will calculate for every square the delta of white attackers to black attackers and sum the deltas
        whitecontrol = 0
        blackcontrol= 0
        for spacesquare in range (64):
            whitecontrol += len(board.attackers(chess.WHITE, spacesquare))
            blackcontrol += len(board.attackers(chess.BLACK, spacesquare))
        control = whitecontrol - blackcontrol

        return control
    
    def get_eval_tension(self, board): 
        
        """
        Based on Matthew P. Tedesco, Ph.D. mptedesco @ https://github.com/mptedesco/python-chess-analysis.git 
        """
        # Tension (or Pressure)
        # very simplistic right now - just a delta of # of attacked pieces for black vs. white
        # when a piece is attacked by the opposing color
            
        spacesquare = 0
        tensionwhite = 0
        tensionblack = 0
        tension = 0
        for spacesquare in range(64):
            if board.piece_at(spacesquare):
                if board.piece_at(spacesquare).color == chess.BLACK:
                    if board.is_attacked_by(chess.WHITE, spacesquare):
                        tensionwhite += 1
                if board.piece_at(spacesquare).color == chess.WHITE:
                    if board.is_attacked_by(chess.BLACK, spacesquare):
                        tensionblack +=1
        tension = tensionwhite - tensionblack

        return tension

    def get_eval_Ksafety(self, board):
        
        """
        Based on Matthew P. Tedesco, Ph.D. mptedesco @ https://github.com/mptedesco/python-chess-analysis.git 
        """
        #King Safety
        # Calculate safety based on a weighted tropism/distance.

        for spacesquare in range(64):
            if board.piece_at(spacesquare):
                if board.piece_at(spacesquare).symbol() == "K":
                    whitekingsquare = spacesquare 
                if board.piece_at(spacesquare).symbol() == "k":
                    blackkingsquare = spacesquare
        
        if whitekingsquare <= 7:    # start figuring out the rank and file for the white king
            whiterank = 0
        elif  whitekingsquare > 7 and whitekingsquare <= 15:
            whiterank = 1
        elif whitekingsquare >15 and whitekingsquare <= 23:
            whiterank = 2
        elif whitekingsquare >23 and whitekingsquare <= 31:
            whiterank = 3
        elif whitekingsquare >31 and whitekingsquare <= 39:
            whiterank = 4
        elif whitekingsquare >39 and whitekingsquare <= 47:
            whiterank = 5
        elif whitekingsquare >47 and whitekingsquare <= 55:
            whiterank = 6
        elif whitekingsquare >55 and whitekingsquare <= 63:
            whiterank = 7
        whitefile = whitekingsquare - whiterank*7 - whiterank

            
        if blackkingsquare <= 7:    # start figuring out the rank and file of the black king
            blackrank = 0
        elif  blackkingsquare > 7 and blackkingsquare <= 15:
            blackrank = 1
        elif blackkingsquare >15 and blackkingsquare <= 23:
            blackrank = 2
        elif blackkingsquare >23 and blackkingsquare <= 31:
            blackrank = 3
        elif blackkingsquare >31 and blackkingsquare <= 39:
            blackrank = 4
        elif blackkingsquare >39 and blackkingsquare <= 47:
            blackrank = 5
        elif blackkingsquare >47 and blackkingsquare <= 55:
            blackrank = 6
        elif blackkingsquare >55 and blackkingsquare <= 63:
            blackrank = 7
        blackfile = blackkingsquare - blackrank*7 - blackrank
        
        
        # now we will loop through all the squares and calculate the sum of the distances x piece values
        # I am using the simple Chebyshev distance as the max of the distance of the ranks or the files
        distancesquare = 0
        whitesafety = 0
        blacksafety = 0
        blackattacked = 0
        whiteattacked = 0
        wmat = 0.1
        bmat = 0.1
        whiteratio = 0
        blackratio = 0
        for distancesquare in range (64):
            if board.piece_at(distancesquare):
                P = board.piece_at(distancesquare).symbol()
            else:
                P = ""
            if distancesquare <= 7:    # figuring out the rank and file
                distancerank = 0
            elif  distancesquare > 7 and distancesquare <= 15:
                distancerank = 1
            elif distancesquare >15 and distancesquare <= 23:
                distancerank = 2
            elif distancesquare >23 and distancesquare <= 31:
                distancerank = 3
            elif distancesquare >31 and distancesquare <= 39:
                distancerank = 4
            elif distancesquare >39 and distancesquare <= 47:
                distancerank = 5
            elif distancesquare >47 and distancesquare <= 55:
                distancerank = 6
            elif distancesquare >55 and distancesquare <= 63:
                distancerank = 7
            distancefile = distancesquare - distancerank*7 - distancerank
            whitedistance = max(abs(whiterank-distancerank), abs(whitefile-distancefile))
            blackdistance = max(abs(blackrank-distancerank), abs(blackfile-distancefile))
            if P == "R":
                blackattacked += self.rook*blackdistance
                whitesafety += self.rook*whitedistance
                wmat += self.rook
            elif P == "B":
                blackattacked += self.bishop*blackdistance
                whitesafety += self.bishop*whitedistance
                wmat += self.bishop
            elif P=="N":
                blackattacked += self.knight*blackdistance
                whitesafety += self.knight*whitedistance
                wmat += self.knight
            elif P=="Q":
                blackattacked += self.queen*blackdistance
                whitesafety += self.queen*whitedistance
                wmat += self.queen
            elif P =="P":
                blackattacked += self.pawn*blackdistance
                whitesafety += self.pawn*whitedistance
                wmat += self.pawn
            elif P == "r":
                blacksafety += self.rook*blackdistance
                whiteattacked += self.rook*whitedistance
                bmat +=self.rook
            elif P == "n":
                blacksafety += self.knight*blackdistance
                whiteattacked += self.knight*whitedistance
                bmat +=self.knight
            elif P == "b":
                blacksafety += self.bishop*blackdistance
                whiteattacked += self.bishop*whitedistance
                bmat +=self.bishop
            elif P=="q":
                blacksafety += self.queen*blackdistance
                whiteattacked += self.queen*whitedistance
                bmat += self.queen
            elif P =="p":
                blacksafety += self.pawn*blackdistance
                whiteattacked += self.pawn*whitedistance
                bmat += self.pawn
        
        # see if king in check and make adjustment to the attacked values adding king value less queen value
        # for each legal king move - this is somewhat arbitrary but intended to penalize a king in check but 
        # reduce the penalty of the king is mobile
        legal = str(board.legal_moves).count("K") + str(board.legal_moves).count("k")
        if board.is_check():
            if board.turn:
                whiteattacked += self.king - self.queen*legal
            else:
                blackattacked += self.king - self.queen*legal
        
        whiteratio = (whitesafety - whiteattacked)/bmat
        blackratio = (blacksafety - blackattacked)/wmat
        safety = blackratio - whiteratio

        return safety


    def load_configuration(self):

        json_file = open('config.json',)
        config = json.load(json_file)
        
        return config

    def get_number_of_pieces(self,board):

        whitepawns = len(board.pieces(1,1))
        whiteknights = len(board.pieces(2,1))
        whitebishops = len(board.pieces(3,1))
        whiterooks = len(board.pieces(4,1))
        whitequeens = len(board.pieces(5,1))
        whiteking = len(board.pieces(6,1))
        blackpawns = len(board.pieces(1,0))
        blackknights = len(board.pieces(2,0))
        blackbishops = len(board.pieces(3,0))
        blackrooks = len(board.pieces(4,0))
        blackqueens = len(board.pieces(5,0))
        blackking = len(board.pieces(6,0))



        total_pieces = whitepawns + whiteknights + whitebishops + whiterooks + whitequeens + whiteking + \
                        blackpawns + blackknights + blackbishops + blackrooks + blackqueens +blackking

        return total_pieces

    def get_piece_value(self,board, square):

        piece = board.piece_at(square)
        # This is for en passant captures where there is no piece in the "to_square"
        if piece == None:
            return self.pawn
        
        else:
            if piece.piece_type == 1:
                return self.pawn
            elif piece.piece_type ==2 :
                return self.knight
            elif piece.piece_type == 3:
                return self.bishop
            elif piece.piece_type == 4:
                return self.rook
            elif piece.piece_type == 5:
                return self.queen
            elif piece.piece_type == 6:
                return self.king
            

    def get_capture_value(self, board, move):
        if board.is_capture(move):
            from_square = move.from_square
            to_square = move.to_square   

            capture_dif = self.get_piece_value(board, to_square) - self.get_piece_value(board, from_square)

            return capture_dif


    # Deprecated
    def get_ordered_captures(self, board):
        legal_captures = board.generate_legal_captures()   
        orders = []
        moves = []
        for move in legal_captures:            
            order= self.get_capture_value(board, move)
            orders.append(order)
            moves.append(move)
        keydict = dict(zip(moves, orders))
        moves.sort(key=keydict.get)
        
        return moves

