import random
from itertools import chain


class Cell:
    def __init__(self, value: int):
        self.mine = False
        self.visited = False
        self.value = value

    def __str__(self):
        if not self.visited or self.mine:
            return ' '
        else:
            return str(self.value)


class Grid:
    def __init__(self, size: int, mines: int):
        self.size = size
        self.grid = [[Cell(0) for _ in range(self.size)] for _ in range(self.size)]
        self.set_mines(mines)

    def __str__(self):
        grid_print = '-'
        for i in range(self.size):
            if i == 0:
                for _ in range(self.size):
                    grid_print += '----'
                grid_print += '\n'

            for k in range(self.size):
                grid_print += '| ' + str(self.grid[i][k]) + ' '
            grid_print += '|\n-'
            for _ in range(self.size):
                grid_print += '----'
            grid_print += '\n'

        return grid_print

    def set_mines(self, mines: int):
        """
        Randomly initialise mines across the grid
        :param mines: integer relating to home many mines to generate
        """

        while mines != 0:
            # Generate x coordinate
            x = random.randint(0, self.size - 1)
            # Generate y coordinate
            y = random.randint(0, self.size - 1)

            if not self.grid[x][y].mine:
                # If not a mine set cell as mine and value as X
                self.grid[x][y].mine = True
                self.grid[x][y].value = 'X'
                mines -= 1

        # Initialise values for all other cells
        self.init_values()

    def init_values(self):
        """
        Assign cell values for all cells based on the amount of adjacent mines in relation to each cell
        """
        for i in range(self.size):
            for j in range(self.size):
                # If not a mine check for mines in all directions
                if not self.grid[i][j].mine:
                    # Assign score based on count of adjacent mines
                    self.grid[i][j].value = self.get_adjacent_cells(i, j)

    def get_adjacent_cells(self, x_coord: int, y_coord: int) -> int:
        """
        Check in all directions for mines and if a mine appears increase result by 1
        :param x_coord: integer
        :param y_coord: integer
        :return: integer the amount of mines adjacent to the current cell
        """
        result = 0

        # loop through all valid adjacent cells and check for mines
        for x, y in [(x_coord + i, y_coord + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i != 0 or j != 0]:
            # ensure in bounds of board
            if 0 <= x < self.size and 0 <= y < self.size:
                # if mine is found increase result by 1
                if self.grid[x][y].mine:
                    result += 1

        return result

    def make_move(self, x_coord: int, y_coord: int):
        """
        Based on coordinates given by player visit cell and unlock all adjacent cells if cell value is > 0 and adjacent
        cell has the same cell value as the current cell
        :param x_coord:
        :param y_coord:
        :return:
        """
        # if cell has already be visited ignore and return true, else update status
        if self.grid[x_coord][y_coord].visited:
            return
        else:
            self.grid[x_coord][y_coord].visited = True

        # loop through all adjacent cells if one is same value and not a mine recursively continue exploration
        for x, y in [(x_coord + i, y_coord + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i != 0 or j != 0]:
            # ensure in bounds of board
            if 0 <= x < self.size and 0 <= y < self.size:
                if not self.grid[x][y].mine:
                    # if same value continue expansion else visit and stop
                    if self.grid[x][y].value == self.grid[x_coord][y_coord].value:
                        self.make_move(x, y)
                    else:
                        self.grid[x][y].visited = True


def play_game():
    """
    Start game and control user input from command line
    """

    # check if input is a valid positive integer, else reprompt
    while True:
        size = input('Choose width of board: ')
        if size.isdigit():
            size = int(size)
            break

    # check if input is a valid positive integer, else reprompt
    while True:
        mines = input('Choose number of mines: ')
        if mines.isdigit():
            mines = int(mines)
            break

    # Initialise game
    win = False
    game_over = False
    board = Grid(size, mines)

    # print blank board
    print(board)

    while not game_over:
        # get x coordinate for move
        while True:
            x = input('Choose x move: ')
            # if not positive int reprompt
            if x.isdigit():
                x = int(x)
                break

        # get y coordinate for move
        while True:
            # if not positive in reprompt
            y = input('Choose y move: ')
            if y.isdigit():
                y = int(y)
                break

        if board.grid[x][y].mine:
            board.grid[x][y].visited = True
            game_over = True
            win = False
        elif not board.grid[x][y].visited:
            board.make_move(x, y)
            print(board)
        else:
            print('Already visited')

        # check if all valid cells visited if so game won
        if all(x.visited or x.mine for x in chain.from_iterable(board.grid)):
            game_over = True
            win = True

    print(board)

    # finish game
    if win:
        print('Winner, winner chicken dinner!')
    else:
        print('Game over, you hit a mine!')


if __name__ == '__main__':
    play_game()
