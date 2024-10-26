from typing import Callable
from BaseClasses import CollectionState


def get_bingo_rule(location, world) -> Callable[[CollectionState], bool]:
    required_keys = extract_bingo_spaces(location)
    return lambda state: all(state.has(key, world.player) for key in required_keys)

def special_rule(world) -> Callable[[CollectionState], bool]:
    all_keys = [f"{chr(row)}{col}" for row in range(ord('A'), ord('E') + 1) for col in range(1, 6)]
    return lambda state: all(state.has(key, world.player) for key in all_keys)

def can_goal(state, player, required_bingos) -> bool:

    # Define all possible Bingo keys (A1 to E5)
    possible_keys = [
        "A1", "A2", "A3", "A4", "A5",
        "B1", "B2", "B3", "B4", "B5",
        "C1", "C2", "C3", "C4", "C5",
        "D1", "D2", "D3", "D4", "D5",
        "E1", "E2", "E3", "E4", "E5"
    ]

    # List of all possible Bingo keys
    possible_bingos = [
        ["A1", "A2", "A3", "A4", "A5"],  # Row A
        ["B1", "B2", "B3", "B4", "B5"],  # Row B
        ["C1", "C2", "C3", "C4", "C5"],  # Row C
        ["D1", "D2", "D3", "D4", "D5"],  # Row D
        ["E1", "E2", "E3", "E4", "E5"],  # Row E
        ["A1", "B1", "C1", "D1", "E1"],  # Column 1
        ["A2", "B2", "C2", "D2", "E2"],  # Column 2
        ["A3", "B3", "C3", "D3", "E3"],  # Column 3
        ["A4", "B4", "C4", "D4", "E4"],  # Column 4
        ["A5", "B5", "C5", "D5", "E5"],  # Column 5
        ["A1", "B2", "C3", "D4", "E5"],  # Diagonal \
        ["A5", "B4", "C3", "D2", "E1"]  # Diagonal /
    ]

    # Collect keys that the player has
    player_keys = []
    for key in possible_keys:  # possible_keys contains all keys (A1, A2, ..., E5)
        if state.has(key, player):
            player_keys.append(key)

    # Count how many Bingos the player has
    bingo_count = 0
    for bingo in possible_bingos:
        if all(key in player_keys for key in bingo):
            bingo_count += 1

    # Check if the number of completed Bingos meets or exceeds the required amount
    return bingo_count >= required_bingos


def extract_bingo_spaces(location):
    # Extract the content within the brackets
    start, end = location[location.index("(") + 1:location.index(")")].split("-")

    # Determine the range of rows and columns
    start_row = start[0]  # 'A', 'B', 'C', etc.
    start_col = int(start[1])  # 1, 2, 3, etc.
    end_row = end[0]  # 'A', 'B', 'C', etc.
    end_col = int(end[1])  # 1, 2, 3, etc.

    spaces = []

    # Generate spaces for horizontal or vertical Bingo
    if start_row == end_row:  # Horizontal Bingo
        col_range = range(start_col, end_col + 1) if start_col < end_col else range(start_col, end_col - 1, -1)
        for col in col_range:
            spaces.append(f"{start_row}{col}")
    elif start_col == end_col:  # Vertical Bingo
        row_range = range(ord(start_row), ord(end_row) + 1) if ord(start_row) < ord(end_row) else range(ord(start_row), ord(end_row) - 1, -1)
        for row in row_range:
            spaces.append(f"{chr(row)}{start_col}")
    else:  # Diagonal Bingo
        row_range = range(ord(start_row), ord(end_row) + 1) if ord(start_row) < ord(end_row) else range(ord(start_row), ord(end_row) - 1, -1)
        col_range = range(start_col, end_col + 1) if start_col < end_col else range(start_col, end_col - 1, -1)
        for row, col in zip(row_range, col_range):
            spaces.append(f"{chr(row)}{col}")

    return spaces
