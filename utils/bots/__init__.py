"""Create a bot in a separate .py and import them here, so that one can simply import
it by from schnapsen.bots import MyBot.
"""
from .rand import RandBot
from .rdeep import RdeepBot
from .bully_bot import BullyBot
from .bot_a import BotA
from .bot_b import BotB
from .bot_c import BotC

__all__ = ["RandBot", "RdeepBot", "BotA", "BotB", "BotC"]