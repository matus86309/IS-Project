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
            return max(valid_moves, key=lambda move: SchnapsenTrickScorer().rank_to_points(move.card.rank))
        # returns lowest rank move if not in phase two
        return min(valid_moves, key=lambda move: SchnapsenTrickScorer().rank_to_points(move.card.rank))
        

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

        # returns a losing move if talon_size == 2 and follower
        if perspective.get_talon_size() == 2:
                non_trumps_sorted = sorted(non_trumps, key= lambda move: rank_to_points(move.card.rank))    
                for move in non_trumps_sorted:
                    if SchnapsenTrickScorer().rank_to_points(move.card.rank) < SchnapsenTrickScorer().rank_to_points(leader_move.card.rank):
                        return move
                    if move.card.suit != leader_move.card.suit:
                        return move
                    
        # returns lowest move if talon_size == 2 and follower
        if perspective.get_talon_size() == 2:
                return min(non_trumps, key= lambda move: SchnapsenTrickScorer().rank_to_points(move.card.rank))
            
        # returns lowest rank move if not in phase two
        return sorted(valid_moves, key=lambda move: SchnapsenTrickScorer().rank_to_points(move.card.rank))[0]
        
