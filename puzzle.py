from tkinter import *
from logic import *
from random import *

SIZE = 500
GRID_LEN = 4
GRID_PADDING = 10

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {   2:"#eee4da", 4:"#ede0c8", 8:"#f2b179", 16:"#f59563", \
                            32:"#f67c5f", 64:"#f65e3b", 128:"#edcf72", 256:"#edcc61", \
                            512:"#edc850", 1024:"#edc53f", 2048:"#edc22e" }
CELL_COLOR_DICT = { 2:"#776e65", 4:"#776e65", 8:"#f9f6f2", 16:"#f9f6f2", \
                    32:"#f9f6f2", 64:"#f9f6f2", 128:"#f9f6f2", 256:"#f9f6f2", \
                    512:"#f9f6f2", 1024:"#f9f6f2", 2048:"#f9f6f2" }
FONT = ("Verdana", 40, "bold")

KEY_UP_ALT = "\'\\uf700\'"
KEY_DOWN_ALT = "\'\\uf701\'"
KEY_LEFT_ALT = "\'\\uf702\'"
KEY_RIGHT_ALT = "\'\\uf703\'"

KEY_UP = "'w'"
KEY_DOWN = "'s'"
KEY_LEFT = "'a'"
KEY_RIGHT = "'d'"

class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)

        #self.gamelogic = gamelogic
        self.playerOneCommands = {
                                    KEY_UP: up, \
                                    KEY_DOWN: down, \
                                    KEY_LEFT: left, \
                                    KEY_RIGHT: right
                                 }

        self.playerTwoCommands = {
                                    KEY_UP_ALT: up, \
                                    KEY_DOWN_ALT: down, \
                                    KEY_LEFT_ALT: left, \
                                    KEY_RIGHT_ALT: right 
                                 }

        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()
        self.playerOneScore = 0
        self.playerTwoScore = 0

        self.turn = 1      # Player's turn (1, 2)

        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg = BACKGROUND_COLOR_GAME, width = SIZE, \
                           height = SIZE)
        background.grid()
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE/GRID_LEN, height=SIZE/GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                # font = Font(size=FONT_SIZE, family=FONT_FAMILY, weight=FONT_WEIGHT)
                t = Label(master=cell, text="[0, 0]", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def gen(self):
        return randint(0, GRID_LEN - 1)

    def init_matrix(self):
        self.matrix = new_game(4)

        self.matrix = addNewValue(self.matrix, 1)
        self.matrix = addNewValue(self.matrix, 1)

    def update_grid_cells(self):
        """
            Updates colours for each cell in grid
        """

        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = self.matrix[i][j][0]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text=str(self.matrix[i][j]), bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(self.matrix[i][j]), bg=BACKGROUND_COLOR_DICT[new_number], fg=CELL_COLOR_DICT[new_number])
        self.update_idletasks()
        
    def key_down(self, event):
        key = repr(event.char)

        if key in self.playerOneCommands and self.turn == 1:

            self.matrix, done, score = self.playerOneCommands[repr(event.char)](self.matrix, self.turn)
            if done:
                self.playerOneScore += score
                print ("Player One Move  Score : ", score)
                print ("Player One Total Score : ", self.playerOneScore)
            else:
                print ("Invalid Move")

            if done:
                self.matrix = addNewValue(self.matrix, self.turn)
                self.update_grid_cells()
                done = False
                if game_state(self.matrix)=='win':
                    self.grid_cells[1][1].configure(text="You",bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Win!",bg=BACKGROUND_COLOR_CELL_EMPTY)
                if game_state(self.matrix)=='lose':
                    self.grid_cells[1][1].configure(text="You",bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Lose!",bg=BACKGROUND_COLOR_CELL_EMPTY)

                self.turn = 2           # Change turn only if valid move

            print ("\n\n")
            print ("====================================")
            print ("Player Two Move")

        elif key in self.playerTwoCommands and self.turn == 2:

            self.matrix, done, score = self.playerTwoCommands[repr(event.char)](self.matrix, self.turn)
            if done:
                self.playerTwoScore += score
                print ("Player Two Move  Score : ", score)
                print ("Player Two Total Score : ", self.playerTwoScore)
            else:
                print ("Invalid Move")

            if done:
                self.matrix = addNewValue(self.matrix, self.turn)
                self.update_grid_cells()
                done = False
                if game_state(self.matrix)=='win':
                    self.grid_cells[1][1].configure(text="You",bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Win!",bg=BACKGROUND_COLOR_CELL_EMPTY)
                if game_state(self.matrix)=='lose':
                    self.grid_cells[1][1].configure(text="You",bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Lose!",bg=BACKGROUND_COLOR_CELL_EMPTY)

                self.turn = 1           # Change turn only if valid move

            print ("\n\n")
            print ("====================================")
            print ("Player One Move")

gamegrid = GameGrid()
