import random

CONST_WALL = 1
CONST_EMPTY = 0
CONST_BOT = 2

class Grid :
	bot = (-1, -1)
	grid = []
	s = [(-1, -1), (-1, 0), (-1, 1),
		(0, -1), (0, 1),
		(1, -1), (1, 0), (1, 1)]
	s2 = [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2),
		(-1, -2), (-1, 2), (0, -2), (0, 2), (1, -2), (1, 2),
		(2, -2), (2, -1), (2, 0), (2, 1), (2, 2)]
	

	def __init__(self, m, n) :	
		self.grid = [[self.wall(x, y, m, n) for y in xrange(n)] for x in xrange(m)]
		self.place_bot(m, n)

	def place_bot(self, m, n) :
		x = random.randint(1, m - 1)
		y = random.randint(1, n - 1)
		self.grid[x][y] = CONST_BOT
		self.bot = (x, y)

	def wall(self, x, y, m, n) :
		if x == 0 or y == 0 or x == m - 1 or y == n - 1 :
			return CONST_WALL
		return CONST_EMPTY

	def print_grid(self) :
		for x in self.grid :
			print x

	def get_location(self) :
		return self.bot

	def get_location_noisy(self) :
		switch = random.randint(0, 9)
		if switch == 0 : # Accurate position, P = 0.1
			return self.bot
		if switch >= 1 or switch <= 4 :
			return self.location_s()
		if switch >= 5 or switch <= 8 :
			return self.location_s2()
		if switch == 9 : # Nothing, P = 0.1
			return ""
		
	def location_s(self) :
		x = random.randint(0, (len(self.s) - 1))
		return (self.bot[0] + self.s[x][0], self.bot[1] + self.s[x][1])

	def location_s2(self) :
		x = random.randint(0, (len(self.s2) - 1))
		return (self.bot[0] + self.s2[x][0], self.bot[1] + self.s2[x][1])
