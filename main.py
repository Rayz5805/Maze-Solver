from graphics import Window
from maze import Maze


def main():
    screen_x = 800
    screen_y = 600
    win = Window(800, 600)

    num_rows = 12
    num_cols = 16
    margin = 50
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows

    print("Generating maze...")
    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, seed=None)
    print("Maze is created!")

    win.solve_button(maze.solve)
    print("Maze is solve!")

    win.wait_for_close()

main()