import io

CONST_EMPTY = 0
CONST_WHITE = 1
CONST_BLACK = -1

class Reversi:
	'''Represents a 8y8 reversi board'''
	e = CONST_EMPTY # Emptx tile 
	w = CONST_WHITE # White tile
	b = CONST_BLACK # Black tile
	board = [[e, e, e, e, e, e, e, e],
	[e, e, e, e, e, e, e, e],
	[e, e, e, e, e, e, e, e],
	[e, e, e, w, b, e, e, e],
	[e, e, e, b, w, e, e, e],
	[e, e, e, e, e, e, e, e],
	[e, e, e, e, e, e, e, e],
	[e, e, e, e, e, e, e, e]]
	white = [(3,3), (4,4)]
	black = [(3,4), (4,3)]

	directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]	

	neytMove = b # First move is black
	
	def toString(self):
		s = "  A B C D E F G H\n"
		c = 1
		for y in self.board :
			s += str(c) + " "
			for x in y :
				if x == self.e :
					s += "- "
				if x == self.w :
					s += "O "
				if x == self.b :
					s += "X "
			c += 1
			s += '\n'
		print s
		print "Black = X, White = O"
		s = ""
		for y in self.white :
			s += self.tupleToString(y) + " "	
		print "White tiles: " + s
		s = ""
		for y in self.black :
			s += self.tupleToString(y) + " "	
		print "Black tiles: " + s

	def getTile(self, y, x):
		return self.board[y][x]

	def getMoves(self):
		moves = {}
		if self.neytMove == self.b :
			for y in self.black :
				for d in self.directions :
					new = (y[0] + d[0], y[1] + d[1])
					temp = []
					while (self.inBounds(new) and
						(self.board[new[0]][new[1]] == self.w)) :
						temp.append(new)
						new = (new[0] + d[0], new[1] + d[1])
					if self.inBounds(new) and (self.board[new[0]][new[1]] == self.e) and len(temp) > 0 :
						if not (new in moves) :
							moves[new] = []
						moves[new].extend(temp)
		return moves

#	def makeMove(self, 

	def setBoard(self, board):
		self.board = board
		white = []
		black = []
		c_y = 0
		c_x = 0
		for y in board :
			for x in y :
				if x == self.w :
					white.append((c_y, c_x))
				elif x == self.b :
					black.append((c_y, c_x))
				c_x += 1
			c_y += 1
			c_x = 0
		self.white = white
		self.black = black

	def inBounds(self, point):
		return point[0] >= 0 and point[0] < 8 and point[1] >= 0 and point[1] < 8

	def tupleToString(self, t):
		return str(chr(65 + t[1])) + str((t[0] + 1))


r = Reversi()
r.toString()
moves = r.getMoves()
for m in moves :
	s = r.tupleToString(m) + " changes: "
	for l in moves[m] :
		s += r.tupleToString(l) + " "
	print s

e = 0
w = 1
b = -1
board = [[e, e, e, e, e, e, e, e],
	[e, e, e, b, w, e, e, e],
	[e, e, e, b, w, e, e, e],
	[e, e, w, w, b, b, e, b],
	[e, e, b, b, w, e, w, w],
	[e, e, e, w, w, b, w, b],
	[e, e, e, e, e, e, e, e],
	[e, e, e, e, e, e, e, e]]

r.setBoard(board)
r.toString()
moves = r.getMoves()
for m in moves :
	s = r.tupleToString(m) + " changes: "
	for l in moves[m] :
		s += r.tupleToString(l) + " "
	print s
