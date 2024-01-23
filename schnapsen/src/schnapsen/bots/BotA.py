from typing import Optional
from schnapsen.game import Bot, PlayerPerspective, Move, SchnapsenTrickScorer, GamePhase, RegularMove


class MyBotA(Bot):

    def get_move(self, perspective: PlayerPerspective, leader_move: Optional[Move]) -> Move:
        valid_moves = [move for move in perspective.valid_moves()]
        non_trumps = [move for move in valid_moves if move.card.suit != perspective.get_trump_suit()]
        rank_to_points = SchnapsenTrickScorer().rank_to_points()
        # returns the first marriage move in valid moves
        for move in valid_moves:
            if move.is_marriage():
                return move
        # returns the first trump exchange move in valid moves
        for move in valid_moves:
            if move.is_trump_exchange():
                return move

        # IF FOLLOWER MOVES:
        if not perspective.am_i_leader():
            # here we play to lose the last trick before phase 2
            if perspective.get_talon_size() == 2:
                non_trumps_sorted = sorted(non_trumps, key= lambda move: rank_to_points(move.card.rank))    
                for move in non_trumps_sorted:
                    if rank_to_points(move.card.rank) < rank_to_points(leader_move.card.rank):
                        return move
                    if move.card.suit != leader_move.card.suit:
                        return move      
            # here we return the lowest value card 
            return min(valid_moves, key= lambda move: rank_to_points(move.card.rank))       

        # IF LEADER MOVES:
        if perspective.get_talon_size() == 2:
                return min(non_trumps, key= lambda move: rank_to_points(move.card.rank))
        
        return max(valid_moves, key=lambda move: rank_to_points(move.card.rank))
