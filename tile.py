from typing import List, Optional, Tuple
from minesweeper_types import BoardType

class Tile():
    # Class representing single tile on the board

    DIRECTIONS = [
        [-1, 1],   [0, 1], [1, 1],
        [-1, 0],           [1, 0],
        [-1, -1], [0, -1], [1, -1]
        ]

    def __init__(self, index: int, num_columns: int, num_rows: int) -> None:
        self.index: int = index
        self.num_columns: int = num_columns
        self.num_rows: int = num_rows
        self.x, self.y = self.getCoordinates(self.index)
        self.value: Optional[int] = None
        self.state: str = 'hidden'
        self.flagged: bool = False
        self.neighbours: List[Tile] = list()
        self.num_unrevealed_neighbours: Optional[int]  = None
        self._mine_chance: Optional[float] = None

    def assign_neighbours(self, board: BoardType):

        for [dx, dy] in Tile.DIRECTIONS:
            newX = self.x + dx
            newY = self.y + dy

            if newX < 0 or newY < 0 or newX >= self.num_columns or newY >= self.num_columns:
                continue
            else:
                newIndex = self.getIndex(newX, newY)
                self.neighbours.append(board[newIndex])
            
    def get_surrounding_info(self, board: BoardType):

        self.num_unrevealed_neighbours = 0

        for [dx, dy] in Tile.DIRECTIONS:
            newX = self.x + dx
            newY = self.y + dy

            if newX < 0 or newY < 0 or newX >= self.num_columns or newY >= self.num_columns:
                continue
            else:
                newIndex = self.getIndex(newX, newY)
                if board[newIndex].state == 'hidden':
                    self.num_unrevealed_neighbours += 1

                
    def getCoordinates(self, index: int):
        # convert index to coordinates
        index = int(index)
        x = index % self.num_columns
        y = index // self.num_columns
        return [x, self.num_columns - 1 - y]

    def getIndex(self, x: int, y: int):
        # get index from coordinates
        return (self.num_columns-1-y)*self.num_columns+(x)
    
    def calculate_mine_chance(self, num_mines: int):
        # calculate mine chance for this cell
        if self._mine_chance == None:
            self._mine_chance = num_mines / (self.num_columns * self.num_rows)
    
    def reveal(self, value: int):
        self.state = 'revealed'
        self.value = value
        self._mine_chance = None
    
    def propagate_mine_chance(self):
        # propagate mine chance for adjacent cells
        if (self.state != 'hidden' and
            self.value is not None and 
            self.value > 0 and 
            self.num_unrevealed_neighbours > 0):

            self._mine_chance = 0

            for neighbour in self.neighbours:
                if neighbour.state == 'revealed':
                    neighbour.mine_chance = 0
                else:
                    neighbour.mine_chance = self.value / self.num_unrevealed_neighbours

        elif self.state == 'revealed':
            self._mine_chance = 0
                

    def __repr__(self) -> str:
        return f"ID: {self.index} | Value: {self.value} | Mine Chance: {self._mine_chance}"
    
    # def __getitem__(self, key):
    #     if key.startswith("t"):
    #         # If the key starts with "t", extract the numerical part and convert it to an integer
    #         tile_index = int(key[1:])
    #         return self.tiles[tile_index]
    #     else:
    #         return self.tiles[tile_index]

    def __setitem__(self, key, tile_data):
        if key.startswith("t"):
            key = int(key[1:])
        self.value, self.state, self.flagged = tile_data

        if self.value == 0:
            self._mine_chance = 0

    @property
    def mine_chance(self):
        return self._mine_chance

    @mine_chance.setter
    def mine_chance(self, new_mine_chance):
        if new_mine_chance > self._mine_chance:
            self._mine_chance = new_mine_chance
        elif self.mine_chance is None:
            self._mine_chance = new_mine_chance
        elif self.state == 'revealed':
            self._mine_chance = 0
        elif self.flagged:
            self._mine_chance = 1


if __name__ == '__main__':
    num_columns = 10
    board = [Tile(index, num_columns) for index in range(0, num_columns * num_columns)]

    # Assign neighbours for each tile
    for tile in board:
        tile.assign_neighbours(board)

    # Print the neighbours of a specific tile (for example, tile at index 0)
    for neighbours in board[11].neighbours:
        print(f"Neighbour: {neighbours.index}, Value: {neighbours.value}")