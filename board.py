from tile import Tile
from minesweeper_types import TileType
from typing import List

class Board():
    # class representing minesweeper game board
    def __init__(self, num_columns, num_rows, num_mines) -> None:
        self.num_columns = num_columns
        self.num_rows = num_rows
        self.num_mines = num_mines
        self.tiles = self.generate_tiles()
    
    def generate_tiles(self):
        board = [Tile(index, self.num_columns, self.num_rows) for index in range(0, self.num_columns * self.num_rows)]
        for tile in board:
            tile.assign_neighbours(board)
            tile.calculate_mine_chance(self.num_mines)
        return board
        
    def reveal(self, index, value):
        self.tiles[index].value = value
        self.tiles[index].state = 'revealed'

    def recalculate(self):
        for tile in self.tiles:
            tile.get_surrounding_info(self)
            # tile.update_values_if_next_to_a_flag()
            tile.propagate_mine_chance()
    
    def get_highest_mine_chances(self) -> List[TileType]:
        # 100% chances exist
        return [tile for tile in self.tiles if tile._mine_chance == 1 and tile.flagged == False]
            
    # def get_lowest_mine_chance(self) -> List[TileType]:
    #     # get best chance tile
    #     best_chance = 1
    #     best_chance_tiles = list()

    #     for tile in self.tiles:

    #         if (tile.mine_chance == 0 and
    #             tile.flagged == False and
    #             tile.state != 'revealed'):

    #             best_chance = tile.mine_chance
    #             best_chance_tiles.append(tile)
            
    #         elif (tile.mine_chance < best_chance and 
    #             tile.state != 'revealed' and
    #             tile.flagged == False):

    #             best_chance = tile.mine_chance
    #             best_chance_tiles = [tile]

    #     return best_chance_tiles

    def get_lowest_mine_chance(self) -> List[TileType]:
        # Get tiles with a mine chance of zero
        zero_chance_tiles = [tile for tile in self.tiles if tile.mine_chance == 0 and not tile.flagged and tile.state != 'revealed']

        if zero_chance_tiles:
            return zero_chance_tiles
        
        else:
            # If there are no zero chance tiles, find the tile with the lowest mine chance
            lowest_chance = min(tile.mine_chance for tile in self.tiles if not tile.flagged and tile.state != 'revealed')
            lowest_chance_tile = next(tile for tile in self.tiles if tile.mine_chance == lowest_chance and not tile.flagged and tile.state != 'revealed')
            return [lowest_chance_tile]

    def __str__(self) -> str:
        return
    
    def __getitem__(self, index):
        return self.tiles[index]

    def __setitem__(self, index, tile_data):
        value, state, flagged = tile_data
        # self.tiles[index].value = value
        # self.tiles[index].state = state
        # self.tiles[index].flagged = flagged
        if index.startswith("t"):
            index = int(index[1:])
        tile = self.tiles[index]
        tile.value, tile.state, tile.flagged = tile_data

if __name__ == '__main__':
    board = Board(10, 10, 15)
    board[0].reveal(1)
