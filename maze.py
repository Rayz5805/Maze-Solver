from cell import Cell
import time
import random

class Maze:
    def __init__(self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
        ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells = [[Cell(self._win) for j in range(self._num_rows)] for i in range(self._num_cols)]
        
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win == None:
            return
        ini_x = self._x1 + self._cell_size_x * i
        ini_y = self._y1 + self._cell_size_y * j
        end_x = ini_x + self._cell_size_x
        end_y = ini_y + self._cell_size_y

        self._cells[i][j].draw(ini_x, ini_y, end_x, end_y)
        self._animate(0.01)

    def _animate(self, dt):
        self._win.redraw()
        time.sleep(dt)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            possible_cells = []
            # get all possible cell to visit
            # right
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                possible_cells.append((i + 1, j))
            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                possible_cells.append((i - 1, j))
            # down
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                possible_cells.append((i, j + 1))
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                possible_cells.append((i, j - 1))

            # return if no target, else choose one
            if len(possible_cells) == 0:
                self._draw_cell(i, j)
                return
            next_i, next_j = random.choice(possible_cells)
            
            # break current and next cell's wall
            # right
            if next_i == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[next_i][next_j].has_left_wall = False
            # left
            elif next_i == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[next_i][next_j].has_right_wall = False
            # down
            elif next_j == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[next_i][next_j].has_top_wall = False
            # up
            elif next_j == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[next_i][next_j].has_bottom_wall = False

            self._break_walls_r(next_i, next_j)

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate(0.04)
        current_cell = self._cells[i][j]
        current_cell.visited = True

        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        
        path_cells = []
        # get all directions of current cell with no wall
        # left
        if i > 0 and not current_cell.has_left_wall:
            path_cells.append((i - 1, j))
        # right
        if i < self._num_cols - 1 and not current_cell.has_right_wall:
            path_cells.append((i + 1, j))
        # up
        if j > 0 and not current_cell.has_top_wall:
            path_cells.append((i, j - 1))
        # down
        if j < self._num_rows - 1 and not current_cell.has_bottom_wall:
            path_cells.append((i, j + 1))

        random.shuffle(path_cells)
        # draw line to not visited cell
        for next_i, next_j in path_cells:
            next_cell = self._cells[next_i][next_j]
            if next_cell.visited == True:
                continue
            current_cell.draw_move(next_cell)

            # make next cell the current cell
            if self._solve_r(next_i, next_j):
                return True
            else:
                current_cell.draw_move(next_cell, undo=True)

        return False