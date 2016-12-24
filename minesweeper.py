### Minesweeper ###
## https://news.ycombinator.com/item?id=8601774 check it out
"""
todo:
-- flood filling!
-- add touch checker function... currently have an object attribute
-- add array searcher function
-- impliment pygame...
	-- to use keypress: arrows to select, enter to break, space to flag
"""
import random
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

clear()

class Square:
	
	def __init__(self, board, x, y):
		self.board = board
		self.x = x
		self.y = y
		self.mine = False
		self.flag = False
		self.show = False
		self.touching = 0
		self.u, self.d, self.l, self.r, self.ul, self.ur, self.dl, self.dr = None, None, None, None, None, None, None, None
		self.cluster = []

	
class Board:
	
	def __init__(self, width, height, mines):
		self.height = height
		self.width = width
		self.mines = mines
		self.playing = True
		self.array = [[Square(self, i, j) for j in range(self.height)] for i in range(self.width)] #builds an array, each item being a Square object
		
		### link building ### ----- SUPER need to rewrite... messed up on UL and UR -----
		"""
		for j in range(self.height): #will assign appropriate links to each Square object in the array
			for i in range(self.width):
				curr_square = self.array[i][j]
				if i != self.width - 1: #if not in last column
					curr_square.r = self.array[i+1][j]
					self.array[i+1][j].l = curr_square
				elif i != 0: #if not in first column
					curr_square.l = self.array[i-1][j]
					self.array[i-1][j].r = curr_square
				if j != self.height - 1: #if not in first row
					curr_square.u = self.array[i][j-1]
					self.array[i][j-1].d = curr_square
					if i != 0: #if not in first column
						curr_square.dl = self.array[i-1][j-1]
						self.array[i-1][j-1].ur = curr_square
					elif i != self.width: #if not in last column
						curr_square.dr = self.array[i+1][j+1]
						self.array[i+1][j+1].ul = curr_square
		"""
		
		for j in range(self.height):
			for i in range(self.width):
				cluster = []
				curr_square = self.array[i][j]
				if i != self.width - 1:
					#print("check1", str(i), str(j))
					curr_square.r = self.array[i+1][j]
					self.array[i+1][j].l = curr_square
					cluster.append(self.array[i+1][j])
				elif i != 0:
					#print("check2", str(i), str(j))
					curr_square.l = self.array[i-1][j]
					self.array[i-1][j].r = curr_square
					cluster.append(self.array[i-1][j])
				if j != 0:
					#print("check3", str(i), str(j))
					curr_square.u = self.array[i][j-1]
					self.array[i][j-1].d = curr_square
					cluster.append(self.array[i][j-1])
					if i != 0:
						#print("check4", str(i), str(j))
						curr_square.ul = self.array[i-1][j-1]
						self.array[i-1][j-1].dr = curr_square
						cluster.append(self.array[i-1][j-1])
					if i != self.width - 1: #temp
						#print("check5", str(i), str(j))
						curr_square.ur = self.array[i+1][j-1]
						self.array[i+1][j-1].dl = curr_square
						cluster.append(self.array[i+1][j-1])
					curr_square.cluster = cluster

		#### mine generation ###
		
		self.mined = []
		for value in range(0, self.mines):
			unique = False
			i = random.randrange(0, self.width)
			j = random.randrange(0, self.heig ht)
			while not unique:
				if self.array[i][j].mine:
					i = random.randrange(0, self.width)
					j = random.randrange(0, self.height)
				else:
					unique = True
					break
			self.array[i][j].mine = True
			self.mined.append(self.array[i][j])
		#print(str(len(self.mined)))
		
		### touch-# assignment ###	
		for j in range(self.height):
			for i in range(self.width):
				curr_square = self.array[i][j]
				touching = 0
				for linked_square in [curr_square.u, curr_square.d, curr_square.l, curr_square.r, curr_square.ul, curr_square.ur, curr_square.dl, curr_square.dr]:
					if linked_square:
						if linked_square.mine:
							touching += 1
				curr_square.touching = touching

	def display(self):
		print("  ", end="")
		for i in range(self.width):
			print(" {} ".format(str(i)), end="")
		print("\n", end="")
		for j in range(self.height):
			row = []
			row.append("{} ".format(str(j)))
			for i in range(self.width):
				curr_square = self.array[i][j]
				if curr_square.show:
					if curr_square.mine and not self.playing:
						row.append("[M]")
					elif curr_square.flag:
						row.append("[X]")
					else:
						row.append("[" + str(curr_square.touching) + "]")
				else:
					row.append("[ ]")
			for item in row:
				print(item, end="")
			print("\n",end="")

### flood fill ###

def flood_fill(board, i, j):
	finished = False
	pointer = board.array[i][j]
	fill = board.array[i][j].cluster
	checked = []
	while not finished:
		pass

"""
def flood_fill(board, i, j): #emulate a recursive function to flood fill and then display accordingly. takes arguments board, i and j
	finished = False
	cluster = board.array[i][j].cluster
	checked = []
	while not finished:
		for pointer in cluster: #need different means of pointer selection
			if pointer.touching == 0 and pointer.mine is False:
				checked.append(pointer)
				cluster.remove(pointer)
				for square in pointer.cluster:
					if square in checked:
						cluster.remove(square)
					elif square.touching == 0 and square.mine is false:
						checked.append(square)
		# edge squares are only ever touching empty squares
"""
### main loop ###

def run():
	clear()
	width = int(input("Width?\n"))
	height = int(input("Height?\n"))
	mines = int(input("Mines?\n"))
	global board
	board = Board(width, height, mines)
	clear()
	board.display()
	while board.playing:
		i = int(input("Which square would you like to examine?\nX-coordinate:\n"))
		j = int(input("Y-coordinate:\n"))
		action = input("[f]lag OR [b]reak?\n")
		invalid = True
		while invalid:
			if board.array[i][j].show or board.array[i][j].flag:
				i = int(input("Square has already been examined. Try again.\nX-coordinate:\n"))
				j = int(input("Y-coordinate:\n"))
				action = input("[f]lag OR [b]reak?\n")
			if "f" in action.lower():
				board.array[i][j].flag = True
				board.array[i][j].show = True
				print(board.array[i][j].flag)
				invalid = False
				break
			elif "b" in action.lower():
				"""
				if board.array[i][j].touching == 0:
					flood_fill(board, i, j)
				"""
				if not board.array[i][j].mine:
					board.array[i][j].show = True
					invalid = False
					break
				else:
					board.playing = False
					invalid = False
					clear()
					board.display()
					
					"""
					### checker ###
					print("Width: ", board.width)
					checker = {"UP: ":board.array[i][j].u, "DOWN: ":board.array[i][j].d, "LEFT: ":board.array[i][j].l, "RIGHT: ":board.array[i][j].r, "UP-LEFT: ":board.array[i][j].ul, "UP-RIGHT: ":board.array[i][j].ur, "DOWN-LEFT: ":board.array[i][j].dl, "DOWN-RIGHT: ":board.array[i][j].dr}
					for attribute in checker:
						if checker[attribute]:
							print(attribute, str(checker[attribute].x) + ", " + str(checker[attribute].y))
						else:
							print(attribute, checker[attribute])
					"""
					break
		if board.playing == False:
			break
		flagged = 0
		for mine in board.mined:
			if mine.flag:
				flagged += 1
		#print(flagged)
		#print(board.mined)
		if flagged == len(board.mined):
			board.playing = False
			break
		for i in range(board.width):
			for j in range(board.height):
				board.array[i][j].show = True
		clear()
		board.display()
	play_again = input("BOOM! Would you like to play again? [Y/N]\n")
	if "y" in play_again.lower():
		run()
	#else:
#		quit()
		
run()

