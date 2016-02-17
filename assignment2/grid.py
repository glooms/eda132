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
		self.m = m
		self.n = n

	def place_bot(self, m, n) :
		x = random.randint(1, m - 2)
		y = random.randint(1, n - 2)
		self.grid[x][y] = CONST_BOT
		self.bot = (x, y)

	def wall(self, x, y, m, n) :
		if x == 0 or y == 0 or x == m - 1 or y == n - 1 :
			return CONST_WALL
		return CONST_EMPTY

	def print_grid(self) :
		for x in self.grid :
			print x

	def set_bot(self, x, y) :
		old_x = self.bot[0]
		old_y = self.bot[1]
		self.grid[old_x][old_y] = CONST_EMPTY
		self.bot = (x, y)
		self.grid[x][y] = CONST_BOT

	def get_location(self) :
		return self.bot

	def get_location_noisy(self) :
		x = random.randint(0, 9)
		if x == 0 : # L, P(L) = 0.1
			return self.bot
		if x >= 1 or x <= 4 : # L_s, P(L_s) = 0.05 * 8 = 0.4
			return self.location_s()
		if x >= 5 or x <= 8 : # L_s2, P(L_s2) = 0.025 * 16 = 0.4
			return self.location_s2()
		if x == 9 : # nothing, P = 0.1
			return "nothing"
		
	def location_s(self) :
		x = random.randint(0, (len(self.s) - 1))
		loc = (self.bot[0] + self.s[x][0], self.bot[1] + self.s[x][1])
		if self.in_bounds(loc[0], loc[1]) :
			return loc
		return "nothing"

	def location_s2(self) :
		x = random.randint(0, (len(self.s2) - 1))
		loc = (self.bot[0] + self.s2[x][0], self.bot[1] + self.s2[x][1])
		if self.in_bounds(loc[0], loc[1]) :
			return loc
		return "nothing"

	def in_bounds(self, x, y) :
		x_in = x > 0 and x < self.m - 1
		y_in = y > 0 and y < self.n - 1
		return x_in and y_in

g = Grid(10, 10)
g.set_bot(8, 8)
g.print_grid()
for x in xrange(10) :
	s = ""
	s += str(g.get_location()) + " "
	s += str(g.get_location_noisy())
	print s
