from typing import Dict, NamedTuple, Optional
from BaseClasses import Item, ItemClassification

class BingoItem(Item):
    game = "APBingo"

class BingoItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler


item_data_table: Dict[str, BingoItemData] = {
    "A1": BingoItemData(
        code=1,
        type=ItemClassification.progression,
    ),
    "A2": BingoItemData(
        code=2,
        type=ItemClassification.progression,
    ),
    "A3": BingoItemData(
        code=3,
        type=ItemClassification.progression,
    ),
    "A4": BingoItemData(
        code=4,
        type=ItemClassification.progression,
    ),
    "A5": BingoItemData(
        code=5,
        type=ItemClassification.progression,
    ),
    "B1": BingoItemData(
        code=6,
        type=ItemClassification.progression,
    ),
    "B2": BingoItemData(
        code=7,
        type=ItemClassification.progression,
    ),
    "B3": BingoItemData(
        code=8,
        type=ItemClassification.progression,
    ),
    "B4": BingoItemData(
        code=9,
        type=ItemClassification.progression,
    ),
    "B5": BingoItemData(
        code=10,
        type=ItemClassification.progression,
    ),
    "C1": BingoItemData(
        code=11,
        type=ItemClassification.progression,
    ),
    "C2": BingoItemData(
        code=12,
        type=ItemClassification.progression,
    ),
    "C3": BingoItemData(
        code=13,
        type=ItemClassification.progression,
    ),
    "C4": BingoItemData(
        code=14,
        type=ItemClassification.progression,
    ),
    "C5": BingoItemData(
        code=15,
        type=ItemClassification.progression,
    ),
    "D1": BingoItemData(
        code=16,
        type=ItemClassification.progression,
    ),
    "D2": BingoItemData(
        code=17,
        type=ItemClassification.progression,
    ),
    "D3": BingoItemData(
        code=18,
        type=ItemClassification.progression,
    ),
    "D4": BingoItemData(
        code=19,
        type=ItemClassification.progression,
    ),
    "D5": BingoItemData(
        code=20,
        type=ItemClassification.progression,
    ),
    "E1": BingoItemData(
        code=21,
        type=ItemClassification.progression,
    ),
    "E2": BingoItemData(
        code=22,
        type=ItemClassification.progression,
    ),
    "E3": BingoItemData(
        code=23,
        type=ItemClassification.progression,
    ),
    "E4": BingoItemData(
        code=24,
        type=ItemClassification.progression,
    ),
    "E5": BingoItemData(
        code=25,
        type=ItemClassification.progression,
    ),

}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
