import random
import json
from utils.bots import RandBot, RdeepBot, BullyBot, BotA, BotB, BotC
from utils.game import SchnapsenGamePlayEngine

class Duel(): 
    """ A class used to run a defined set of matches to 7 game points between 2 bots
    """
    def __init__(self, bot1, bot2):
        """ 
        :param: match_results: results of the current match used to store gamepoints between individual games
        :param: victories: stores the amount of games won by individual players
        :param: total results: stores the total amount of game points achieved in all matches
        :param: bots: a tuple of the 2 bots participating in the Duel
        """
        self.match_results = None
        self.victories = {str(bot1): 0, str(bot2): 0}
        self.total_results = {str(bot1): 0, str(bot2): 0}
        self.bots = [bot1, bot2]

    def playMatches(self, n):
        """ A function that runs n matches and stores the results in a specified format
        :param: n: the amount of matches to be played
        :return: duel results in the form of a dictionary, with the amount of total victories in the Duel, 
            as well as total game points achieved and logs of all individual games' results
        """
        # play n matches, while providing each match with a unique identifier
        # Note: Keep this here for correct return value
        logs = [self.playMatch(mId + 1) for mId in range(n)]

        return {
            "duel-results": {
                "match-victories": self.victories,
                "total-game-points": self.total_results
            },
            "progress-logs": logs
        }

    def playMatch(self, matchID):
        """ Play a match of schnapsen to 7 game points
        :param: matchID: a numeric value used to distinguish individual matches played in a duel
        :return: results of the match as well as the amount of game points achieved so far
        """
        # delete the results of the previous match and start from 0 on both sides
        self.match_results = {str(self.bots[0]): 0, str(self.bots[1]): 0}
        # set the leader of the first trick so that a different one begins every match
        firstBot = str(self.bots[matchID % 2])

        # Play games until one of the players has achieved 7 points
        while all(p < 7 for p in self.match_results.values()):
            # play a game
            winner_id, game_points, score = self.play_game(firstBot)
            # log the results
            self.match_results[str(winner_id)] += game_points
            # set the winner of the match as the leader of the next game's first trick
            firstBot = str(winner_id)
            
        self.__updateTotalResults()

        return {"match-id": matchID, "match-results": self.match_results, "total-results": self.total_results}

    def play_game(self, firstBot = None):
        """ Play a single game starting with the specified player
        :return: a tuple containting (id of the winner, game points the winner has achieved, score of the game)
        """

        if str(self.bots[0]) == firstBot :
            return SchnapsenGamePlayEngine().play_game(self.bots[0], self.bots[1], random.Random(random.randint(0, 200)))
        else:
            return SchnapsenGamePlayEngine().play_game(self.bots[1], self.bots[0], random.Random(random.randint(0, 200)))

    def __updateTotalResults(self):
         """ After each completed match, run this function to update the final stats of the Duel
         """
         
         self.victories[[ name for name, score in self.match_results.items() if score >= 7][0]] += 1
         self.total_results = { key: self.total_results[key] + self.match_results[key] for key in self.match_results.keys()  }


### Change this to specify the number of matches played in each duel
numberOfGames = 10

### Bots to be tested
testedBots = [
    BotA( name="BotA"),
    BotB( name="BotB"),
    BotC( name="BotC")
]
### Bots to test againts
bots = [
    RandBot(rand=random.Random(random.randint(0, 200)), name="RandBot"),
    RdeepBot(num_samples = 20, depth=5, rand=random.Random(random.randint(0, 200)), name="RdeepBot"),
    BullyBot(rand=random.Random(random.randint(0, 200)), name="BullyBot")
]
          

for i in range(len(testedBots)):
    for j in range(len(bots)):
    
        # Play n matches and get the results
        bot1 = testedBots[i]
        bot2 = bots[j]
        results = Duel(bot1, bot2).playMatches(numberOfGames)

        # Output results into a text file
        path = "test_results/"
        with open(f"{path}results_{str(bot1)}_vs_{str(bot2)}.json", "w") as file:
            json.dump(results, file)     
             
print("Test completed")