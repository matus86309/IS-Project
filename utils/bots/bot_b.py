from typing import Optional
from ..game import Bot, PlayerPerspective, Move, SchnapsenTrickScorer

class BotB(Bot):

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

        non_trumps = [move for move in valid_moves if move.card.suit != perspective.get_trump_suit()]
        rank_to_points = SchnapsenTrickScorer().rank_to_points

        # IF FOLLOWER MOVES:
        if not perspective.am_i_leader():
            leader_suit_moves = [ move for move in valid_moves if move.cards[0].suit == leader_move.cards[0].suit ]
            
            # here we play to lose the last trick before phase 2
            if perspective.get_talon_size() == 2:
                non_trumps_sorted = sorted(non_trumps, key= lambda move: rank_to_points(move.cards[0].rank))    
                for move in non_trumps_sorted:
                    if rank_to_points(move.cards[0].rank) < rank_to_points(leader_move.cards[0].rank):
                        return move
                    if move.card.suit != leader_move.cards[0].suit:
                        return move      
        
            # here we return the lowest card that is higher than leader move which has the same suit as the leader suit
            if len(leader_suit_moves) > 0:
                higher_than_leader_suit_moves = [move for move in leader_suit_moves if rank_to_points(move.cards[0].rank) > rank_to_points(leader_move.cards[0].rank)]
                if len (higher_than_leader_suit_moves) > 0:
                    return min(higher_than_leader_suit_moves, key=lambda move: rank_to_points(move.cards[0].rank))

            # here we return the lowest non trump suit move 
            if len(non_trumps) > 0:
                return min(non_trumps, key=lambda move: rank_to_points(move.cards[0].rank))
        
            # here we return the lowest value card 
            return min(valid_moves, key= lambda move: rank_to_points(move.cards[0].rank))       


        # IF LEADER MOVES:
        if perspective.get_talon_size() == 2:
                return min(non_trumps, key= lambda move: rank_to_points(move.cards[0].rank))
        
        return max(valid_moves, key=lambda move: rank_to_points(move.cards[0].rank))
