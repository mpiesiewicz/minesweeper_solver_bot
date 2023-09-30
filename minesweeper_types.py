from typing import List, Optional

class TileType:
    index: int
    num_columns: int
    num_rows: int
    x: int
    y: int
    value: Optional[str]
    state: str
    flagged: bool
    neighbours: List['TileType']
    num_unrevealed_neighbours: Optional[int]
    mine_chance: Optional[float]

class BoardType:
    num_columns: int
    num_rows: int
    num_mines: int
    tiles: List['TileType']