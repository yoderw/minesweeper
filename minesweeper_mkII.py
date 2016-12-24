"""
to do:
-- comments, clarity, elegance
-- change loops to new structure
-- impliment floodfill
-- make mine generation a function and call after first selection
-- make mine generation more interesting

"""

import random, os
from flood_fill import flood_fill

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Square: #square object, used in Board array constructor
    def __init__(self, board, x, y): #takes board and position
        self.board = board
        self.x = x
        self.y = y
        self.mine = False #square is mined
        self.flag = False #flagged by player
        self.show = False #show in screen draw
        self.value = 0 #number of touching squares
        self.u, self.d, self.l, self.r, self.ul, self.ur, self.dl, self.dr = None, None, None, None, None, None, None, None #tracks which other square objects self is touching
        self.touching = [] #list of above objects. (may be used in floodfill)

    def touch_check(self):
        for attribute in [self.u, self.d, self.l, self.r, self.ul, self.ur, self.dl, self.dr]:
            if attribute: self.touching.append(attribute)

class Board:
    def __init__(self, width, height, mines):
        self.height = height
        self.width = width
        self.mines = mines
        self.playing = True
        self.array = [[Square(self, x, y) for x in range(self.height)] for y in range(self.width)] #builds the array with a square object at each coordinate pair
        self.mined = []

        for i in range(self.width*self.height): ##touch assignment ##
            x, y = i//self.height, i%self.height
            curr_square = self.array[x][y]
            if x != self.width - 1: #if square not in last column
                curr_square.r = self.array[x+1][y]
                curr_square.r.l = curr_square
            elif x != 0: #if square not in first column
                curr_square.l = self.array[x-1][y]
                curr_square.l.r = curr_square
            if y != 0: #if square not in first row
                curr_square.u = self.array[x][y-1]
                curr_square.u.d = curr_square
                if x != 0: #if square not in first column
                    curr_square.ul = self.array[x-1][y-1]
                    curr_square.ul.dr = curr_square
                if x != self.width - 1: #if square not in last column
                    curr_square.ur = self.array[x+1][y-1]
                    curr_square.ur.dl = curr_square

        for i in range(self.width*self.height):
            x, y = i//self.height, i%self.height
            self.array[x][y].touch_check()

    def populate(self, ex_x, ex_y): #populates board with mines and value assignments
        exclude = (ex_x, ex_y)
        if self.mines:
            for i in range(0, self.mines + 1): ## mine generation ##
                x, y = random.randrange(0, self.width), random.randrange(0, self.height)
                while True:
                    if self.array[x][y].mine or (x, y) == exclude:
                        x, y = random.randrange(0, self.width), random.randrange(0, self.height)
                    else:
                        break
                self.array[x][y].mine = True
                self.mined.append(self.array[x][y])

        for i in range(self.width*self.height): ## value assignment ##
            x, y = i//self.height, i%self.height
            curr_square = self.array[x][y]
            value = 0
            for linked_square in [curr_square.u, curr_square.d, curr_square.l, curr_square.r, curr_square.ul, curr_square.ur, curr_square.dl, curr_square.dr]:
                if linked_square and linked_square.mine: value += 1
            curr_square.value = value

    def display(self): #prints array to the console. shows value of squares w/ .show = True (squares flagged or broke by player
        #clear()
        print("  ", end="")
        for x in range(self.width):
            print(" {} ".format(str(x)), end="")
        print("\n", end="")
        for y in range(self.height):
            row = []
            row.append("{} ".format(str(y)))
            for x in range(self.width):
                curr_square = self.array[x][y]
                if curr_square.show:
                    if curr_square.mine and not self.playing: row.append("[M]")
                    elif curr_square.flag: row.append("[X]")
                    else: row.append("[" + str(curr_square.value) + "]")
                else: row.append("[ ]")
            for item in row: print(item,end="")
            print("\n",end="")

    def examine(self): #asks player for coordinate pair and action to be performed (flag:= flag square as mine, break:= break square to show value). performs action on chosen square
        x = int(input("Which square would you like to examine?\nX-coordinate:\n"))
        y = int(input("Y-coordinate:\n"))
        action = input("[f]lag OR [b]reak?\n")
        if not self.mined:
            self.populate(x, y)
        while True:
            if board.array[x][y].show or board.array[x][y].flag:
                x = int(input("Square has already been examined. Try again.\nX-coordinate:\n"))
                y = int(input("Y-coordinate:\n"))
                action = input("[f]lag OR [b]reak?\n")
            else:
                board.array[x][y].show = True
                break
        if "f" in action.lower():
            board.array[x][y].flag = True
        elif "b" in action.lower():
            if not board.array[x][y].mine:
                self.array[x][y].show = True
                if board.array[x][y].value == 0:
                    flood_fill(self, x, y)
            else:
                board.playing = False
                for i in range(self.width*self.height):
                    x, y = i//self.height, i%self.height
                    self.array[x][y].show = True
        self.display()

def run(): ## main loop ##
    clear()
    width = int(input("Width?\n"))
    height = int(input("Height?\n"))
    mines = int(input("Mines?\n"))
    global board
    board = Board(width, height, mines)
    board.display()
    while board.playing: board.examine()

b = Board(3,3,0)
