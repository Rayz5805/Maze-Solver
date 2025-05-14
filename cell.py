from graphics import Line, Point

class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win

        self.visited = False

    def draw(self, x1, y1, x2, y2):
        if self._win == None:
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2

        line = Line(Point(x1, y1), Point(x1, y2))
        if self.has_left_wall:
            self._win.draw_line(line)
        else:
            self._win.draw_line(line, "white")
        
        line = Line(Point(x2, y1), Point(x2, y2))
        if self.has_right_wall:
            self._win.draw_line(line)
        else:
            self._win.draw_line(line, "white")
        
        line = Line(Point(x1, y1), Point(x2, y1))
        if self.has_top_wall:
            self._win.draw_line(line)
        else:
            self._win.draw_line(line, "white")
        
        line = Line(Point(x1, y2), Point(x2, y2))
        if self.has_bottom_wall:
            self._win.draw_line(line)
        else:
            self._win.draw_line(line, "white")

    def draw_move(self, to_cell, undo=False):
        line_color = "grey" if undo else "red"

        self_half_lenght = abs(self._x2 - self._x1) // 2
        self_center_x = self._x1 + self_half_lenght
        self_center_y = self._y1 + self_half_lenght

        other_half_lenght = abs(to_cell._x2 - to_cell._x1) // 2
        other_center_x = to_cell._x1 + other_half_lenght
        other_center_y = to_cell._y1 + other_half_lenght

        line = Line(Point(self_center_x, self_center_y), Point(other_center_x, other_center_y))
        self._win.draw_line(line, line_color)
