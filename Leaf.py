import chess
from dataclasses import dataclass

@dataclass
class Leaf:

    board: chess.Board = None
    move: chess.Move = None
    score: int = 0