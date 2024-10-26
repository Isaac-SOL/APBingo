from dataclasses import dataclass
from Options import Toggle, Option, Range, Choice, ItemSet, OptionSet, PerGameCommonOptions

class RequiredBingos(Range):
    """The number of Bingo's required to goal, min is 1, max is 12"""
    range_start = 1
    range_end = 12
    default = 1
    display_name = "Required Bingos"

@dataclass
class BingoOptions(PerGameCommonOptions):
    required_bingos: RequiredBingos