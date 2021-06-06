import chess
import sys
from collections import Counter
from evaluation import evaluation


class Minimax():
    def __init__(self):
        self.eval=evaluation()


    def minimax_play(self, depth, board,isMaximizing):
        
        bestMoveFinal, bestMove, _ = self.minimaxRoot(depth, board,isMaximizing)
        
        print("Best score: " ,str(bestMove))
        print("Best move: ",str(bestMoveFinal))
        return bestMoveFinal
        

    def minimax_train(self, depth, board, isMaximizing):
        
        _, _, bestLeaf = self.minimaxRoot(depth, board, isMaximizing)
        features_eval = self.eval.get_features_eval(bestLeaf)
        
        return features_eval, bestLeaf
    
    
    def minimaxRoot(self, depth, board,isMaximizing):
        possibleMoves = self.get_ordered_legal_moves(board)
        if isMaximizing:
            best_value = -9999 
        else:
            best_value = 9999
        best_move = None
        bestLeaf = None
        for x in possibleMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            value, leaf = self.minimax(depth - 1, board,-9998,9998, not isMaximizing)
            if (isMaximizing) and (value > best_value):
                best_value = value
                bestLeaf = leaf
                best_move = move
            if (not isMaximizing) and (value < best_value):
                best_value = value
                bestLeaf = leaf
                best_move = move
            board.pop()
           
                

        return best_move, best_value, bestLeaf

    def minimax(self, depth, board, alpha, beta, is_maximizing):
        possibleMoves = self.get_ordered_legal_moves(board)

        if(depth == 0) or not possibleMoves: 
            if self.is_possbile_captures(board):
                return self.quiesce(alpha, beta, board), board

            else:
                return self.eval.get_evaluation(board), board
        
        if(is_maximizing):
            best_value = -9997
            best_leaf = board
            for x in possibleMoves:
                move = chess.Move.from_uci(str(x))
                board.push(move)
                new_value, new_leaf = self.minimax(depth - 1, board,alpha,beta, not is_maximizing)
                if best_value < new_value:
                    best_value = new_value
                    best_leaf = new_leaf
                board.pop()
                alpha = max(alpha,best_value)
                if beta <= alpha:
                    return best_value, best_leaf
            return best_value, best_leaf
        else:
            best_value = 9997
            best_leaf = board
            for x in possibleMoves:
                move = chess.Move.from_uci(str(x))
                board.push(move)
                new_value, new_leaf = self.minimax(depth - 1, board,alpha,beta, not is_maximizing)
                if best_value > new_value:
                    best_value = new_value
                    best_leaf = new_leaf
                board.pop()
                beta = min(beta,best_value)
                if(beta <= alpha):
                    return best_value, best_leaf
            return best_value, best_leaf


    def quiesce(self, alpha, beta, board):
        stand_pat = self.eval.get_evaluation(board)
        
        if( stand_pat >= beta ):
            return beta
        if( alpha < stand_pat ):
            alpha = stand_pat

        if self.is_possbile_captures(board):
                
            legal_captures = self.get_ordered_legal_captures(board)       
            for move in legal_captures:            
                board.push(move)        
                score = self.quiesce( -beta, -alpha, board )
                board.pop()

                if( score >= beta ):
                    return beta
                if( score > alpha ):
                    alpha = score  
            return alpha

        return stand_pat # if there are no possible moves returns score = beta

    def quiesce_return_safe(self, alpha, beta, board) -> int:

        score: int = 0

        stand_pat = self.eval.get_evaluation(board)
        
        if( stand_pat >= beta ):
            score = beta
        else:

            if( alpha < stand_pat ):
                # alpha, score = stand_pat
                alpha = stand_pat
                score = alpha
                score = ""
            if self.is_possbile_captures(board):

                legal_captures = board.generate_legal_captures()        
                for move in legal_captures:
                    if self.eval.get_capture_value(board, move) >= 0:
                        board.push(move)        
                        score = self.quiesce( -beta, -alpha, board )
                        board.pop()

                        if( score >= beta ):
                            score = beta
                            break
                        if( score > alpha ):
                            alpha = score  

        return score


    def is_possbile_captures(self, board):
        legal_captures = board.generate_legal_captures()
        
        return Counter(legal_captures)

    def get_ordered_legal_moves(self, board):
        checks =[]
        captures = []
        others = []
        legal_moves = board.legal_moves
        for x in legal_moves:
            move = chess.Move.from_uci(str(x))
            if board.gives_check(move):
               checks.append(x)
            elif board.is_capture(move):
               captures.append(x)
            else:
                others.append(x)
        
        return checks + captures + others



    def get_ordered_legal_captures(self, board):
        best_captures = []
        equal_captures = []
        minor_captures = []
        legal_captures = board.generate_legal_captures()
        for x in legal_captures:
            move = chess.Move.from_uci(str(x))
            if self.eval.get_capture_value(board, move) > 0:
                best_captures.append(x)
            elif self.eval.get_capture_value(board, move) == 0:
                equal_captures.append(x)
            else:
                minor_captures.append(x)
        
        return best_captures + equal_captures + minor_captures




    
    

