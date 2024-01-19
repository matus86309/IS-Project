from typing import Optional
from schnapsen.game import Bot, PlayerPerspective, Move, SchnapsenTrickScorer, GamePhase, RegularMove


class MyBotA(Bot):

    def get_move(self, perspective: PlayerPerspective, leader_move: Optional[Move]) -> Move:
        valid_moves = [move for move in perspective.valid_moves()]

        # returns the first marriage move in valid moves
        for move in valid_moves:
            if move.is_marriage():
                return move
        
        # returns the first trump exchange move in valid moves
        for move in valid_moves:
            if move.is_trump_exchange():
                return move

        # returns highest rank move if in phase two
        if perspective.get_phase() == GamePhase.TWO:
            return sorted(valid_moves, key=lambda move: SchnapsenTrickScorer().rank_to_points(move.card.rank), 
                                   reverse=True)[0]
        # returns lowest rank move if not in phase two
        return sorted(valid_moves, key=lambda move: SchnapsenTrickScorer().rank_to_points(move.card.rank))[0]
        

class MyBotB(Bot):

    def get_move(self, perspective: PlayerPerspective, leader_move: Optional[Move]) -> Move:
        valid_moves = [move for move in perspective.valid_moves()]

        # returns the first marriage move in valid moves
        for move in valid_moves:
            if move.is_marriage():
                return move
        
        # returns the first trump exchange move in valid moves
        for move in valid_moves:
            if move.is_trump_exchange():
                return move

        # returns highest rank move if in phase two
        if perspective.get_phase() == GamePhase.TWO:
            return sorted(valid_moves, key=lambda move: SchnapsenTrickScorer().rank_to_points(move.card.rank), 
                                   reverse=True)[0]
        
        non_trumps = [move for move in valid_moves if move.card.suit != perspective.get_trump_suit()]

        # returns lowest rank move that isn't of the trump suit
        if perspective.get_talon_size() == 2:
                return min(non_trumps, key= lambda move: SchnapsenTrickScorer().rank_to_points(move.card.rank))
            
        # returns lowest rank move if not in phase two
        return sorted(valid_moves, key=lambda move: SchnapsenTrickScorer().rank_to_points(move.card.rank))[0]
        
