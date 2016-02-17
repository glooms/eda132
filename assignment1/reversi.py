import io
import random
import time

CONST_EMPTY = 0
CONST_WHITE = 1
CONST_BLACK = -1

class Reversi:
	'''Represents a 8x8 reversi board'''
	e = CONST_EMPTY # Empty tile 
	w = CONST_WHITE # White tile
	b = CONST_BLACK # Black tile

	# We global constants for the 3 different tile states: empty, blach and white.
	# A 8x8 matrix for the board, seperate lists with coordinates of all black
	# and white tiles. And a list of possible changes to a nodes position to get to
	# its neighbours called directions.
	# Furthermore, we used a stack called history to compute a search tree and traverse
	# (more than prune) it with the alphabeta function.
	# In addition, we tracked the available moves for the player who's turn it is with
	# a dictionary (python for map) of all the different moves available and what they
	# change. (A coordinate for the placement of the tile and a list of coordinates 
	# that will change.) (The move chosen is then added to the history stack.)

	# The -0.02 next to timelimit is somewhat arbitrary but seemed to give close to
	# max time spent while not overshooting, in most cases. 

	def __init__(self, timelimit) :
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

		self.whosMove = b # First move is black

		self.history = []

		self.moves = {}

		self.timelimit = timelimit - 0.02
	
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
		if self.whosMove == self.b :
			print "Black's move"
		else :
			print "White's move"
		print "Black = X, White = O"
		print "White has %d tiles" % len(self.white)
		print "Black has %d tiles\n" % len(self.black) 

	def getTile(self, y, x):
		return self.board[y][x]

	# This function traverses the board by first finding
	# a tile of the same color that is to be placed and
	# then moving out in the eight directions from it searching
	# for tiles of the opposite color that are connected
	# followed by an empty tile. These empty tiles are added
	# to the "moves" map so that if the same tile is found 
	# multiple times, the list of changes that that move would
	# bring are joined, thus giving the whole impact of the move.

	def possibleMoves(self):
		self.moves = {}
		if self.whosMove == self.b :
			search = self.black
		else :
			search = self.white
		for x in search :
			for d in self.directions :
				new = (x[0] + d[0], x[1] + d[1])
				temp = []
				while (self.inBounds(new) and
					(self.board[new[0]][new[1]] == -self.whosMove)) :
					temp.append(new)
					new = (new[0] + d[0], new[1] + d[1])
				if self.inBounds(new) and (self.board[new[0]][new[1]] == self.e) and len(temp) > 0 :
					if not (new in self.moves) :
						self.moves[new] = []
					self.moves[new].extend(temp)

	def getMoves(self):
		return self.moves
	
	def passTurn(self):
		self.history.append((0, 0, 0))
		self.whosMove = -self.whosMove
		self.possibleMoves()

	# This is where the action happens.
	# Moves are made and added to the history
	# stack.

	def makeMove(self, tile):
		move = self.moves[tile]
		self.changeTile(tile)
		for m in move :
			self.changeTile(m)
		self.history.append((tile, move, self.whosMove))
		self.whosMove = -self.whosMove
		self.possibleMoves()

	# This is how we can generate a tree with
	# our otherwise rigid structure. We undo our
	# last move, arriving at our previous state.
	# This is done with the help of the stack
	# history.

	def undoLastMove(self):
		move = self.history.pop()
		tile = move[0]
		if move[2] == self.b :
			self.black.remove(tile)
		else :
			self.white.remove(tile)
		self.board[tile[0]][tile[1]] = self.e
		changes = move[1]
		l = len(self.history)
		for m in changes :
			self.changeTile(m)
		self.whosMove = move[2]
		self.possibleMoves()
		
	# Helper function, for makeMove and undoLastMove

	def changeTile(self, tile):
		status = self.board[tile[0]][tile[1]]
		if status == self.b :
			self.black.remove(tile)
		elif status == self.w :
			self.white.remove(tile)
		self.board[tile[0]][tile[1]] = self.whosMove
		if self.whosMove == self.b :
			self.black.append(tile)
		else :
			self.white.append(tile)

	# This is a rather standard implementation of alphabeta function
	# Instead of infinity and negative infinity as v, alpha and beta
	# we chose to use 64 and -64 which represents the min and max of
	# our utility function, the difference in amount of tiles between
	# the player to be maximized and the player to minized.
	# To solve the time constraint we simply return the worst value
	# for every new function call that is close to exceeding the time
	# limit.

	def calcMove(self, depth, alpha, beta, maximize, color, parent, startTime) :
		if (time.time() - startTime) >= self.timelimit : 
			if maximize :
				return -64
			return 64
		if depth == 0 :
			score = self.tally()
			if color == self.b :
				return -score
			return score
		v = 0
		if maximize :
			v = -64
			for m in self.moves :
				self.makeMove(m)
				res = self.calcMove(depth - 1, alpha, beta, False, color, m, startTime)
				if v < res :
					v = res
					if parent is "root" :
						self.optimalMove = m
				self.undoLastMove()
				alpha = max(alpha, v)
				if beta <= alpha :
					break
		else :
			v = 64
			for m in self.moves :
				self.makeMove(m)
				v = min(v, self.calcMove(depth - 1, alpha, beta, False, color, m, startTime))
				self.undoLastMove()
				beta = min(beta, v)
				if beta <= alpha :
					break
		return v

		
	def getOptimalMove(self):
		return self.optimalMove

	def inBounds(self, point):
		return point[0] >= 0 and point[0] < 8 and point[1] >= 0 and point[1] < 8

	# Just a pretty print function. If it looks funny, it's because it is.
	# It converts e.g. (5, 0) to A6. 

	def tileToString(self, t):
		return str(chr(65 + t[1])) + str((t[0] + 1))

	# Used as our utility function.

	def tally(self) :
		blackScore = len(self.black)
		whiteScore = len(self.white)
		return whiteScore - blackScore
	

print "Welcome to reversi!"
timelimit = input("Input a time limit in seconds, minimum 0.2\n")
depth = input("What recursive depth would you like for your adversary?\nWe suggest something around 3-5.\n")
play = input("Enter a 0 if you want to play or a 1 for a simulation\n")
r = Reversi(timelimit)
r.possibleMoves()
noMoves = False
flag = True
for x in range(64) :
	r.toString()
	moves = r.getMoves()
	if flag :
		flag = False
		if len(moves) == 0 :
			if noMoves :
				r.tally()
				r.toString()
				break
			r.passTurn()
			noMoves = True
		elif play == 0 :		
			for i, m in enumerate(moves) :
				s = str(i) + " " + r.tileToString(m) + " changes: "
				for l in moves[m] :
					s += r.tileToString(l) + " "
				print s
			number = input("Enter a number: ")
			if number == 20 :
				print "Undoing move"
				r.undoLastMove()
				continue
			move = moves.keys()[number]
			print r.tileToString(move)
			r.makeMove(move)
		elif play == 1 :
			l = len(moves)
			choice = random.randint(0, l - 1)
			move = moves.keys()[choice]
			r.makeMove(move)
			noMoves = False 
	else :
		flag = True
		if len(moves) == 0 :
			if noMoves :
				r.tally()
				r.toString()
				break
			r.passTurn()
			noMoves = True
		else :
			start = time.time()
			r.calcMove(depth, -64, 64, True, CONST_BLACK, "root", start)
			print "-----------------------------------------"
			print "Time elapsed: %f" % (time.time() - start)
			print "-----------------------------------------"
			m = r.getOptimalMove()
			r.makeMove(m)
			noMoves = False

