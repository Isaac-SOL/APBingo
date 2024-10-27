from typing import List, Dict, Any

from BaseClasses import Region, Item, ItemClassification, Entrance, Tutorial, MultiWorld
from worlds.AutoWorld import World
from worlds.LauncherComponents import Component, components, Type, launch_subprocess
from .Items import BingoItem, item_data_table, item_table
from .Locations import BingoLocation, location_data_table, location_table
from .Options import BingoOptions
from .Regions import region_data_table
from .Rules import get_bingo_rule, special_rule, can_goal


def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="APBingoClient")


components.append(Component(
    "APBingo Client",
    "APBingoClient",
    func=launch_client,
    component_type=Type.CLIENT
))


class BingoWorld(World):
    """Randomized Bingo!"""

    game = "APBingo"
    options: BingoOptions
    options_dataclass = BingoOptions
    location_name_to_id = location_table
    item_name_to_id = item_table
    board_locations = []

    def create_item(self, name: str) -> BingoItem:
        return BingoItem(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        item_pool: List[BingoItem] = []
        for name, item in item_data_table.items():
            if item.code:
                item_pool.append(self.create_item(name))

        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        # Create regions.
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Create locations.
        for region_name, region_data in region_data_table.items():
            region = self.get_region(region_name)
            region.add_locations({
                location_name: location_data.address for location_name, location_data in location_data_table.items()
                if location_data.region == region_name}, BingoLocation)
            region.add_exits(region_data_table[region_name].connecting_regions)

    def set_rules(self) -> None:
        bingo_names = [
            "Bingo (A1-A5)-0",
            "Bingo (A1-A5)-1",
            "Bingo (B1-B5)-0",
            "Bingo (B1-B5)-1",
            "Bingo (C1-C5)-0",
            "Bingo (C1-C5)-1",
            "Bingo (D1-D5)-0",
            "Bingo (D1-D5)-1",
            "Bingo (E1-E5)-0",
            "Bingo (E1-E5)-1",
            "Bingo (A1-E1)-0",
            "Bingo (A1-E1)-1",
            "Bingo (A2-E2)-0",
            "Bingo (A2-E2)-1",
            "Bingo (A3-E3)-0",
            "Bingo (A3-E3)-1",
            "Bingo (A4-E4)-0",
            "Bingo (A4-E4)-1",
            "Bingo (A5-E5)-0",
            "Bingo (A5-E5)-1",
            "Bingo (A1-E5)-0",
            "Bingo (A1-E5)-1",
            "Bingo (E1-A5)-0",
            "Bingo (E1-A5)-1",
        ]

        all_keys = [f"{chr(row)}{col}" for row in range(ord('A'), ord('E') + 1) for col in range(1, 6)]

        for bingo in bingo_names:
            self.get_location(bingo).access_rule = get_bingo_rule(bingo, self)
            self.get_location(bingo).item_rule = lambda item: item.name not in all_keys

        self.get_location("Bingo (ALL)").access_rule = special_rule(self)
        self.get_location("Bingo (ALL)").item_rule = lambda item: item.name not in all_keys

        # Completion condition.
        self.multiworld.completion_condition[self.player] = lambda state: can_goal(state,self.player, self.options.required_bingos)

    def find_locations(self):

        self.board_locations = []
        squares = [
            "A1", "A2", "A3", "A4", "A5",
            "B1", "B2", "B3", "B4", "B5",
            "C1", "C2", "C3", "C4", "C5",
            "D1", "D2", "D3", "D4", "D5",
            "E1", "E2", "E3", "E4", "E5"
        ]

        for square in squares:
            board_location = self.multiworld.find_item(square, self.player)
            self.board_locations.append(str(board_location))


    def fill_slot_data(self) -> Dict[str, Any]:

        self.find_locations()

        return {
            "requiredBingoCount": self.options.required_bingos.value,
            "boardLocations": self.board_locations,
        }

