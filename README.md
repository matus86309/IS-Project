# Schnapsen bot performance testing environment #

This package has been designed to run matches to 7 game points following the standard schnapsen ruleset. It consists of files *game.py* and *deck.py* required to run the games, a set of bots, against which new bots can be tested, and a *test.py* file which contains the testing framework. 
This package makes use of files from a [Schnapsen package](https://github.com/intelligent-systems-course/schnapsen/blob/main/README.md) to run the game and test the bots. For practical reasons, only the essential files were included instead of the whole package. These files remain unchanged, and therefore, the whole repository is compatible with the Schnapsen package. 

## Terminology ## 
This package uses terms created for better clarity

- game 
    a single game of Schnapsen to 66 points
- match 
    a set of games of Schnapsen to 7 game points
- duel
    a set of matches between 2 bots

## Getting started ##

The *test.py* file has been set up as a demo to test bots BotA, BotB and BotC in Duels against RandBot, Rdeep and BullyBot.The number of matches played in every duel can be set in the *numberOfMatches* variable highlighted in the *test.py* file. For every duel, a new file is created in the *test_results* directory, containing the duel results, as well as a log of every individual game containing the results of the game and a sum of game points of all previous games to keep track of the progress. The names of the files are created based on the names given to the bots, therefore **it is essential that all of the bots have a unique name**, otherwise the results will get overwritten. 

To see the results of bots BotA, BotB and BotC against RandBot, Rdeep and BullyBott it is only required to clone the github repository and then run the *test.py* file. If you wish to specify the number of games played in each duel you can specify the number in the *numberOfGames* variable highlighted in the code. Immediately after you can find the list of the bots tested, as well as a list of bots to be tested against. By adding or removing a bot from this list it is possible to increase or decrease the amount of tests run.

In case you wish to make further modifications, please reffer to the inline code documentation or in case of the schnapsen package files to [Schnapsen package home page](https://github.com/intelligent-systems-course/schnapsen/blob/main/README.md)

## Adding new bots ## 

To add a new bot simply copy the file into *utils/bots*, refference it in the *utils/bots/\_\_init\_\_.py* file as shown and import it in the test.py file using local imports.

```Python

from utils.bots import nameOfYourBot

```

Then add it into the list of bots to be tested or bots to be tested against, as highlighted in the *test.py* file.

## Test results ##

For every duel, a new file is created in the *test_results* directory, containing the duel results, as well as a log of every individual game containing the results of the game and a sum of game points of all previous games to keep track of the progress. The names of the files are created based on the names given to the bots, therefore **it is essential that all of the bots have a unique name**, otherwise the results will get overwritten. 

In the test result files an overall statistic can be found at the beginning, but in case you wish to create your own statistic based on the results, the data is stored in json format and can therefore be easily worked with further. For better readability of this code we advise the use of a code formatter, after the use of which the data will become more clear. Such a formatter is included in VSCode text editor by default. 

An example of the test results file structure: 

```json
{
  "duel-results": {
    "match-victories": { "BotA": 7, "BullyBot": 3 },
    "total-game-points": { "BotA": 65, "BullyBot": 44 }
  },
  "progress-logs": [
    {
      "match-id": 1,
      "match-results": { "BotA": 5, "BullyBot": 7 },
      "total-results": { "BotA": 5, "BullyBot": 7 }
    },
    {
      "match-id": 2,
      "match-results": { "BotA": 7, "BullyBot": 0 },
      "total-results": { "BotA": 12, "BullyBot": 7 }
    }
    // ...
  ]
}
```

Note: As you can see, each match has an id indicating the number of the match, and also contains a progress tracker of total results, which can be used for easier creation of charts. 