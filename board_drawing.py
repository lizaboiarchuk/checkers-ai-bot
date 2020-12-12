import time
import tkinter
from main import game
import math


# Board Drawing manager
class BDManager:
    # Properties
    _needsUpdate = True

    def __init__(self):
        # Initialize parameters
        self.ROWS = 8
        self.COLS = 8
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 800
        self.col_width = self.WINDOW_WIDTH / self.COLS
        self.row_height = self.WINDOW_HEIGHT / self.ROWS
        # Game
        self.game = game
        # Drawing
        self._draw_board_only()
        # Run main loop
        self.root.mainloop()

    def _draw_board_only(self):
        self.root = tkinter.Tk()
        self.c = tkinter.Canvas(self.root, width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT, borderwidth=5,
                                background='white')
        self.c.pack()
        self.tiles = set()

        # Print dark square
        for i in range(self.ROWS):
            for j in range(self.COLS):
                if (i + j) % 2 == 1:
                    self.c.create_rectangle(i * self.row_height, j * self.col_width,
                                            (i + 1) * self.row_height, (j + 1) * self.col_width, fill="gray",
                                            outline="gray")

        # Print grid lines
        for i in range(self.ROWS):
            self.c.create_line(0, self.row_height * i, self.WINDOW_WIDTH, self.row_height * i, width=2)
            self.c.create_line(self.col_width * i, 0, self.col_width * i, self.WINDOW_HEIGHT, width=2)

        # Place checks on the board
        self.update_board()

    def update_board(self):
        if self.game.is_over():
            return
        # remove old pieces
        for tile in self.tiles:
            self.c.delete(tile)
        self.tiles -= self.tiles
        # draw new
        for piece in self.game.board.pieces:
            if piece.captured:
                continue

            color = "red" if piece.player == 1 else "black"
            j = piece.get_row()
            i = piece.get_column() * 2 + 1 if j % 2 == 0 else piece.get_column() * 2
            tile = self.c.create_oval(j * self.col_width + 10, i * self.row_height + 10,
                                      (j + 1) * self.col_width - 10, (i + 1) * self.row_height - 10,
                                      fill=color)
            self.tiles.add(tile)
            self.c.tag_raise(tile)
            if piece.king:
                self.draw_king_icon(i,j)
        # make GUI updates board every second
        self.root.after(1, self.update_board)

    def draw_king_icon(self, i, j):
        def submit_tile(tile):
            self.tiles.add(tile)
            self.c.tag_raise(tile)

        slip = math.sqrt(2) * self.row_height - (self.row_height - 20)
        left =  self.c.create_line(j * self.col_width + slip, i * self.row_height + slip, 
                                    (j + 1) * self.col_width - slip, (i + 1) * self.row_height - slip,
                                    width=5, fill="white")
        submit_tile(left)
        right =  self.c.create_line((j + 1) * self.col_width - slip, i * self.row_height + slip,  
                                    j * self.col_width + slip, (i + 1) * self.row_height - slip,
                                    width=5, fill="white")
        submit_tile(right)