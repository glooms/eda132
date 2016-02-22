import random
import bot

S = [(-1, -1), (-1, 0), (-1, 1),
	(0, -1), (0, 1),
	(1, -1), (1, 0), (1, 1)]
	
S_2 = [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2),
		(-1, -2), (-1, 2), (0, -2), (0, 2), (1, -2), (1, 2),
		(2, -2), (2, -1), (2, 0), (2, 1), (2, 2)]

class Grid :
	def __init__(self, m, n) :	
		self.grid = [[0 for y in xrange(n)] for x in xrange(m)]
		self.history = []	
		self.place_bot(m, n)
		self.m = m
		self.n = n

	def place_bot(self, m, n) :
		x = random.randint(1, m - 1)
		y = random.randint(1, n - 1)
		self.bot = bot.Bot(x, y, self)

	def print_grid(self) :
		s = "  "
		for x in xrange(len(self.grid)) :
			s += " " + str(x)
		s += "\n"
		c = 0
		for x in self.grid :
			s += " " + str(c) + " "
			for y in x :
				if y == 0 :
					s += "- "
				else :
					s += "b "
			s += "\n"
			c += 1
		print s

	def change(self, x, y) :
		if self.grid[x][y] == 0 :
			self.grid[x][y] = 1 
			self.history.append((x, y))
		else :
			self.grid[x][y] = 0 

	def next(self) :
		self.bot.move()
		return (self.get_location_noisy(),
			self.bot.get_heading())

	def set_bot(self, x, y) :
		self.bot.move_to(x, y)

	def get_bot(self) :
		return self.bot

	def get_location(self) :
		return self.bot.get_loc()

	def get_location_noisy(self) :
		x = random.randint(0, 9)
		if x == 0 : # L, P(L) = 0.1
			return self.bot.get_loc()
		if x >= 1 and x <= 4 : # L_s, P(L_s) = 0.05 * 8 = 0.4
			return self.location_s()
		if x >= 5 and x <= 8 : # L_s2, P(L_s2) = 0.025 * 16 = 0.4
			return self.location_s2()
		if x == 9 : # nothing, P = 0.1
			return "nothing"
		
	def location_s(self) :
		r = random.randint(0, (len(S) - 1))
		loc = self.bot.get_loc()
		x = loc[0] + S[r][0]
		y = loc[1] + S[r][1]
		if self.in_bounds(x, y) :
			return (x, y)
		return "nothing"

	def location_s2(self) :
		r = random.randint(0, (len(S_2) - 1))
		loc = self.bot.get_loc()
		x = loc[0] + S_2[r][0]
		y = loc[1] + S_2[r][1]
		if self.in_bounds(x, y) :
			return (x, y)
		return "nothing"

	def in_bounds(self, x, y) :
		x_in = x >= 0 and x < self.m
		y_in = y >= 0 and y < self.n
		return x_in and y_in

	def print_history(self) :
		print self.history
