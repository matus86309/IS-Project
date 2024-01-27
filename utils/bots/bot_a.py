from typing import Optional
from ..game import Bot, PlayerPerspective, Move, SchnapsenTrickScorer


class BotA(Bot):

    def get_move(self, perspective: PlayerPerspective, leader_move: Optional[Move]) -> Move:
        valid_moves = [move for move in perspective.valid_moves()]

        # point scorer method but shortened for ease of use
        rank_to_points = SchnapsenTrickScorer().rank_to_points

        # IF FOLLOWER MOVES:
        if not perspective.am_i_leader():  
            # here we return the lowest value card 
            return min(valid_moves, key= lambda move: rank_to_points(move.cards[0].rank))       

        # IF LEADER MOVES:
        # here we return the highest ranking card
        return max(valid_moves, key=lambda move: rank_to_points(move.cards[0].rank))
