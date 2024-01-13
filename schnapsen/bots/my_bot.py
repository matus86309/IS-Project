from typing import Optional
from schnapsen.game import Bot, PlayerPerspective, Move, SchnapsenTrickScorer, GamePhase, RegularMove

class MyBot(Bot):
    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name)

    def get_move(self, player_perspective: PlayerPerspective, leader_move: Optional[Move], ) -> Move:
        rank_to_points = SchnapsenTrickScorer().rank_to_points
        trump_suit = player_perspective.get_trump_suit()

        valid_moves = player_perspective.valid_moves()
        non_trump_suit_moves = [ move for move in valid_moves if move.cards[0].suit != trump_suit ]
        trump_suit_moves = [ move for move in valid_moves if move.cards[0].suit == trump_suit ]

        marriage_moves = [move for move in valid_moves if move.is_marriage()]
        if len(marriage_moves) > 0:
            # play a marriage if possible
            return marriage_moves[0].as_marriage()
        
        trump_exchange_moves = [move for move in valid_moves if move.is_trump_exchange()]
        if len(trump_exchange_moves) > 0:
            # play a trump exchange if possible
            return trump_exchange_moves[0].as_trump_exchange()
        
        #
        #   Follower part
        #

        if not player_perspective.am_i_leader():
            leader_suit_moves = [ move for move in valid_moves if move.cards[0].suit == leader_move.cards[0].suit ]
            non_leader_non_trump_suit_moves = [ move for move in valid_moves if move.cards[0].suit != leader_move.cards[0].suit and move.cards[0].suit != trump_suit ]

            if player_perspective.get_talon_size() == 2:
                if len(non_leader_non_trump_suit_moves) > 0:
                    # lose the last trick before the deck runs out
                    if len(leader_suit_moves) > 0 and rank_to_points(leader_suit_moves[0].cards[0].rank) < rank_to_points(leader_move.cards[0].rank):
                            return leader_suit_moves[0]
                    return min(non_leader_non_trump_suit_moves, key= lambda move: rank_to_points(move.cards[0].rank))

            # Go through plays following leading suit
            if len(leader_suit_moves) > 0:
                # return the lowest card of leader suit higher than played card if possible, lowest otherwise
                higher_leader_suit_moves = [move for move in leader_suit_moves if rank_to_points(move.cards[0].rank) > rank_to_points(leader_move.cards[0].rank) ]
                if len(higher_leader_suit_moves) > 0:
                    return min(higher_leader_suit_moves, key= lambda move: rank_to_points(move.cards[0].rank))
                
            if rank_to_points(leader_move.cards[0].rank) >= 10 and len(trump_suit_moves):
                # play lowest trump card if the value of the card is higher or equal to 10
                return min(trump_suit_moves, key= lambda move: rank_to_points(move.cards[0].rank))

            if len(non_trump_suit_moves) > 0:
                # return the lowest card of non-trump suit
                return min(non_trump_suit_moves, key= lambda move: rank_to_points(move.cards[0].rank))
            
            # in other cases play lowest possible (trump) card
            return min(valid_moves, key= lambda move: rank_to_points(move.cards[0].rank))
        
        #
        #   Leader part
        #
        
        if player_perspective.get_talon_size() == 2:
            if len(non_trump_suit_moves) > 0:
                # lose the last trick before the deck runs out
                return min(non_trump_suit_moves, key= lambda move: rank_to_points(move.cards[0].rank))
            
        if player_perspective.get_phase() == GamePhase.ONE:


            if len(non_trump_suit_moves) > 0:
                # play lowest non-trump card
                return min(non_trump_suit_moves, key= lambda move: rank_to_points(move.cards[0].rank))
            # play lowest (trump) card - not necessary, wince one can't have 5 trump cards on hand
            return min(valid_moves, key= lambda move: rank_to_points(move.cards[0].rank))
        
        suits = ["HEARTS", "SPADES", "CLUBS", "DIAMONDS"]

        # cards on my hand divided by suit
        my_hand_by_suit = {suit: [] for suit in suits}
        for card in player_perspective.get_hand():
            my_hand_by_suit[str(card.suit)].append(card)

        # cards on the opponents hand divided by suit
        opponent_hand_by_suit = {suit: [] for suit in suits}
        for card in player_perspective.get_opponent_hand_in_phase_two():
            opponent_hand_by_suit[str(card.suit)].append(card)
        
        if any(len(opponent_hand_by_suit[suit]) == 0 and suit != str(trump_suit) for suit in suits):
            suit_i_have_but_opponent_doesnt = [ suit for suit in suits if len(my_hand_by_suit[suit]) > 0 and len(opponent_hand_by_suit[suit]) == 0]
            cards_of_suit_i_have_but_opponent_doesnt = [card for card in player_perspective.get_hand() if str(card.suit) in suit_i_have_but_opponent_doesnt]
            
            if len(cards_of_suit_i_have_but_opponent_doesnt) > 0:
                # if an opponent doesn't have a card of a suit and I do and it isn't a trump suit, play the one of them with lowest value
                return RegularMove(min(cards_of_suit_i_have_but_opponent_doesnt, key= lambda card: rank_to_points(card.rank)))

        if len(trump_suit_moves) > 0:
            return max(trump_suit_moves, key= lambda move: rank_to_points(move.cards[0].rank))
        
        return max(valid_moves, key= lambda move: rank_to_points(move.cards[0].rank))