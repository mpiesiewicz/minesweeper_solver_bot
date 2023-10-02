from bs4 import BeautifulSoup
import settings
from playwright.sync_api import sync_playwright
import math
from board import Board
from typing import Tuple

class Solver():

    URL = settings.URL

    def __init__(self) -> None:
        self.browser, self.page = self.initialize()
        self.num_columns, self.num_rows, self.num_mines = self.analyze_game_settings()
        self.board = Board(self.num_columns, self.num_rows, self.num_mines)
        self.grid_data = self.update_board()
        self.game_on = True
        self.game_state = None

    def initialize(self):
        p = sync_playwright().start()
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(Solver.URL)
        return browser, page

    def analyze_game_settings(self) -> Tuple[int, int, int]:
        html = self.page.content()
        soup = BeautifulSoup(html, 'html.parser')

        # Extract game difficulty
        num_mines = int(soup.find(id = 'mines-counter').text)

        # Extract the grid style to get the number of columns
        grid_style = soup.find('div', id='board')['style']
        num_columns = int(grid_style.split('(')[1].split(',')[0])

        # Count the number of child elements to get the number of rows
        grid_cells = soup.find_all('div', class_='tile hidden-tile')
        num_rows = len(grid_cells) // num_columns

        self.num_rows = num_rows
        self.num_columns = num_columns
        self.num_mines = num_mines

        return num_columns, num_rows, num_mines

    def update_board(self):

        # Capture the Minesweeper grid HTML
        page_html = self.page.inner_html('body')

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(page_html, 'html.parser')
    
        # Extract the grid cells and their IDs
        grid_cells = soup.find_all('div', class_='tile')

        for cell in grid_cells:
            cell_id = cell['id']

            # assign value
            if cell.text == '':
                value = 'unknown' 
            elif cell.text == '🚩':
                value = 'mine'
            elif cell.text == '💥':
                pass
            else :
                value = int(cell.text)

            state = 'hidden' if 'hidden-tile' in cell['class'] else 'revealed'
            flagged = True if cell.text == '🚩' else False
            self.board[cell_id] = (value, state, flagged)

        self.board.recalculate()
    
    def start(self):
        game_on = True
        self.select_difficulty('easy')

        # reveal first tile
        self.reveal(0)

        while game_on:

            mines = self.board.get_highest_mine_chances()
            print(f'found 100% mines: {mines}')
            if not mines:
                print(f'no 100%s, calculating lowest chance...')
                lowest_mine_chance = self.board.get_lowest_mine_chance()
                print(f'lowest chance: {lowest_mine_chance[0]}')
                for tile in lowest_mine_chance:
                    self.reveal(tile.index)

            else:
                for tile in mines:
                    self.flag(tile.index)

            self.update_board()

        print('done')


    def reveal(self, index):
        id = f"#t{index}"
        self.page.click(id)
        # self.update_board()

    def flag(self, index):
        id = f"#t{index}"
        self.page.click(id, button='right')
        # self.update_board()

    # def after_click(self):
    #     self.update_board()

    def select_difficulty(self, difficulty):
        self.page.select_option('#level-drop-down', difficulty)
        self.analyze_game_settings()
        self.update_board()
        self.board = Board(self.num_columns, self.num_rows, self.num_mines)

    def get_unrevealed_neighbours(self, index):

        unrevealed_neighbours = 0

        directions = [
        [-1, -1], [-1, 0],  [-1, 1],
        [0, -1] ,            [0, 1],
        [1, -1] ,  [1, 0],   [1, 1]
        ]

        x, y = self.getCoordinates(index)

        for [dx, dy] in directions:
            newX = x + dx
            newY = y + dy

            if newX < 0 or newY < 0 or newX >= self.num_columns or newY >= self.num_columns:
                continue
            newIndex = self.getIndex(newX, newY)
            if self.grid_data[f"t{newIndex}"]['state'] == 'hidden':
                unrevealed_neighbours += 1

        return unrevealed_neighbours
        
    def getCoordinates(self, index):
        # convert index to coordinates
        index = int(index)
        x = index % self.num_columns
        y = math.floor(index / self.num_columns)
        return [x, self.num_columns - 1 - y]

    def getIndex(self, x, y):
        # get index from coordinates
        return (self.num_columns-1-y)*self.num_columns+(x)