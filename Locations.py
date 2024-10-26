from typing import Dict, NamedTuple, Optional
from BaseClasses import Location


class BingoLocation(Location):
    game = "APBingo"


class BingoLocationData(NamedTuple):
    region: str
    address: Optional[int] = None


location_data_table: Dict[str, BingoLocationData] = {

    "Bingo (A1-A5)-0": BingoLocationData(region="Bingo Board", address=1),
    "Bingo (A1-A5)-1": BingoLocationData(region="Bingo Board", address=2),

    "Bingo (B1-B5)-0": BingoLocationData(region="Bingo Board", address=3),
    "Bingo (B1-B5)-1": BingoLocationData(region="Bingo Board", address=4),

    "Bingo (C1-C5)-0": BingoLocationData(region="Bingo Board", address=5),
    "Bingo (C1-C5)-1": BingoLocationData(region="Bingo Board", address=6),

    "Bingo (D1-D5)-0": BingoLocationData(region="Bingo Board", address=7),
    "Bingo (D1-D5)-1": BingoLocationData(region="Bingo Board", address=8),

    "Bingo (E1-E5)-0": BingoLocationData(region="Bingo Board", address=9),
    "Bingo (E1-E5)-1": BingoLocationData(region="Bingo Board", address=10),

    "Bingo (A1-E1)-0": BingoLocationData(region="Bingo Board", address=11),
    "Bingo (A1-E1)-1": BingoLocationData(region="Bingo Board", address=12),

    "Bingo (A2-E2)-0": BingoLocationData(region="Bingo Board", address=13),
    "Bingo (A2-E2)-1": BingoLocationData(region="Bingo Board", address=14),

    "Bingo (A3-E3)-0": BingoLocationData(region="Bingo Board", address=15),
    "Bingo (A3-E3)-1": BingoLocationData(region="Bingo Board", address=16),

    "Bingo (A4-E4)-0": BingoLocationData(region="Bingo Board", address=17),
    "Bingo (A4-E4)-1": BingoLocationData(region="Bingo Board", address=18),

    "Bingo (A5-E5)-0": BingoLocationData(region="Bingo Board", address=19),
    "Bingo (A5-E5)-1": BingoLocationData(region="Bingo Board", address=20),

    "Bingo (A1-E5)-0": BingoLocationData(region="Bingo Board", address=21),
    "Bingo (A1-E5)-1": BingoLocationData(region="Bingo Board", address=22),

    "Bingo (E1-A5)-0": BingoLocationData(region="Bingo Board", address=23),
    "Bingo (E1-A5)-1": BingoLocationData(region="Bingo Board", address=24),

    "Bingo (ALL)": BingoLocationData(region="Bingo Board", address=25),
}


location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}
