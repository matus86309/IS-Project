from typing import Optional
from schnapsen.game import Bot, PlayerPerspective, Move, SchnapsenTrickScorer, GamePhase, RegularMove
from schnapsen.game import Card, Suit

class BotC(Bot):
    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name)

    def get_move(self, perspective: PlayerPerspective, leader_move: Optional[Move], ) -> Move:
        rank_to_points = SchnapsenTrickScorer().rank_to_points
        trump_suit = perspective.get_trump_suit()
        
        valid_moves = perspective.valid_moves()
        non_trump_suit_moves = [move for move in valid_moves if move.card.suit != trump_suit]
        
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
            leader_suit_moves = [move for move in valid_moves if move.cards[0].suit == leader_move.card.suit]
            # here we play to lose the last trick before phase 2            
            if perspective.get_talon_size() == 2:
                non_trumps_sorted = sorted(non_trump_suit_moves, key=lambda move: rank_to_points(move.card.rank))    
                for move in non_trumps_sorted:
                    if rank_to_points(move.card.rank) < rank_to_points(leader_move.card.rank):
                        return move
                    if move.card.suit != leader_move.card.suit:
                        return move
                    
            # here we return the lowest card that is higher than leader move which has the same suit as the leader suit
            if len(leader_suit_moves) > 0:
                higher_than_leader_suit_moves = [move for move in leader_suit_moves if rank_to_points(move.card.rank) > rank_to_points(leader_move.card.rank)]
                if len (higher_than_leader_suit_moves) > 0:
                    return min(higher_than_leader_suit_moves, key=lambda move: rank_to_points(move.card.rank))

            # here we return the lowest non trump suit move 
            if len(non_trump_suit_moves) > 0:
                return min(non_trump_suit_moves, key=lambda move: rank_to_points(move.card.rank))
            
            # here we play our lowest card
            return min(valid_moves, key= lambda move: rank_to_points(move.card.rank))    
           
        # IF LEADER MOVES:

        # here we play to lose the last trick before phase 2
        if perspective.get_talon_size() == 2:
            return non_trumps_sorted[0]

        # here we play our lowest non trump move if we're in phase 1
        if perspective.get_phase() == GamePhase.ONE:
            return min(non_trump_suit_moves, key=lambda move: rank_to_points(move.card.rank))
     
        suits = [Suit.HEARTS, Suit.SPADES, Suit.CLUBS, Suit.DIAMONDS]
        hand_by_suit = {suit: [move.card for move in valid_moves if move.card.suit == suit] for suit in suits}
        opponent_hand_by_suit = {suit: [card for card in perspective.get_opponent_hand_in_phase_two().cards if card.suit == suit] for suit in suits}
        
        # here we play a the lowest value of our suits that the opponent doesn't have, if any
        for my_suit, opponent_suit in zip(hand_by_suit, opponent_hand_by_suit):
            if len(hand_by_suit[my_suit]) > len(opponent_hand_by_suit[opponent_suit]) and len(opponent_hand_by_suit[opponent_suit]) == 0:
                return RegularMove(min(hand_by_suit[my_suit], key=lambda card: rank_to_points(card.rank)))
            
        # here we play our highest card 
        return max(valid_moves, key=lambda move: rank_to_points(move.cards[0].rank))