import io
import random
import csv

CONST_EMPTY = 0
CONST_WHITE = 1
CONST_BLACK = -1

class Reversi:
	'''Represents a 8x8 reversi board'''
	e = CONST_EMPTY # Empty tile 
	w = CONST_WHITE # White tile
	b = CONST_BLACK # Black tile

	def __init__(self) :
		e = self.e
		w = self.w
		b = self.b
		self.board = [[e, e, e, e, e, e, e, e],
		[e, e, e, e, e, e, e, e],
		[e, e, e, e, e, e, e, e],
		[e, e, e, w, b, e, e, e],
		[e, e, e, b, w, e, e, e],
		[e, e, e, e, e, e, e, e],
		[e, e, e, e, e, e, e, e],
		[e, e, e, e, e, e, e, e]]
		self.white = [(3,3), (4,4)]
		self.black = [(3,4), (4,3)]

		self.directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]	

		self.nextMove = b # First move is black

		self.history = []

		self.sumOptions = 0.0
	
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
		for x in self.white :
			s += self.tileToString(x) + " "	
		print "White tiles: " + s
		s = ""
		for x in self.black :
			s += self.tileToString(x) + " "	
		print "Black tiles: " + s
		
		s = ""
		for x in self.history :
			if x[0] == 0 : 
				continue
			s += "(" + self.tileToString(x[0]) + ", "
			if x[2] == self.b :
				s += "X) "
			else :
				s += "O) "
		print "History: " + s

	def getTile(self, y, x):
		return self.board[y][x]

	def getMoves(self):
		self.moves = {}
		if self.nextMove == self.b :
			search = self.black
		else :
			search = self.white
		for x in search :
			for d in self.directions :
				new = (x[0] + d[0], x[1] + d[1])
				temp = []
				while (self.inBounds(new) and
					(self.board[new[0]][new[1]] == -self.nextMove)) :
					temp.append(new)
					new = (new[0] + d[0], new[1] + d[1])
				if self.inBounds(new) and (self.board[new[0]][new[1]] == self.e) and len(temp) > 0 :
					if not (new in self.moves) :
						self.moves[new] = []
					self.moves[new].extend(temp)
		self.sumOptions += len(self.moves)
		return self.moves
	
	def passTurn(self):
		self.history.append((0, 0, 0))
		self.nextMove = -self.nextMove

	def makeMove(self, tile):
		move = self.moves[tile]
		self.changeTile(tile)
		for m in move :
			self.changeTile(m)
		self.history.append((tile, move, self.nextMove))
		self.nextMove = -self.nextMove

	def changeTile(self, tile):
		status = self.board[tile[0]][tile[1]]
		if status == self.b :
			self.black.remove(tile)
		elif status == self.w :
			self.white.remove(tile)
		self.board[tile[0]][tile[1]] = self.nextMove
		if self.nextMove == self.b :
			self.black.append(tile)
		else :
			self.white.append(tile)
			 
		

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

	def tileToString(self, t):
		return str(chr(65 + t[1])) + str((t[0] + 1))

	def tally(self) :
		blackScore = len(self.black)
		whiteScore = len(self.white)
		print "Black has %d tiles" % blackScore
		print "White has %d tiles" % whiteScore
		if blackScore > whiteScore :
			print "Black wins!"
		elif blackScore == whiteScore :
			print "It's a draw!"
		else :
			print "White wins!"
		avgBranch = self.sumOptions / len(self.history)
		return avgBranch

avg = []
for times in range(1000) :
	r = Reversi()
	c = 0
	flag = False
	for x in range(64) :
		if flag :
			flag = False
			r.toString()
			moves = r.getMoves()
			if len(moves) == 0 :
				print "No moves available"
				if c == 1 :
					r.tally()
					break
				r.passTurn()
				c += 1
			else :
				for i, m in enumerate(moves) :
					s = str(i) + " " + r.tileToString(m) + " changes: "
					for l in moves[m] :
						s += r.tileToString(l) + " "
					print s
			
				number = input("Enter a number: ")
				move = moves.keys()[number]
				print r.tileToString(move)
				r.makeMove(move)
				c = 0
		else :
#			flag = True
			moves = r.getMoves()
			if len(moves) == 0 :
				if c == 1 :
					avg.append(r.tally())
					break
				r.passTurn()
				c += 1
			else :
				l = len(moves)
				choice = random.randint(0, l - 1)
				move = moves.keys()[choice]
#				for m in moves :
#					if len(moves[move]) < len(moves[m]) :
#						move = m
				r.makeMove(move)
				c = 0
with open('test.csv', 'w', 1) as fp:
	a = csv.writer(fp, delimiter=',')
	data=[]
	for x in avg :
		data.append([x])
	a.writerows(data)
