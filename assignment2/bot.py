import random

# Headings up, down, left, right
HEADINGS = [(1, 0), (-1, 0), (0, -1), (0, 1)]

def h_to_string(h) :
	if HEADINGS[0] is h :
		return "UP"
	if HEADINGS[1] is h :
		return "DOWN"
	if HEADINGS[2] is h :
		return "LEFT"
	if HEADINGS[3] is h :
		return "RIGHT"
	return ""
	

class Bot :
	loc = (-1, -1)
	possible_headings = set()
	heading = (1, 0) # h_t
	
	def __init__(self, x, y, grid) :
		self.grid = grid
		self.loc = (x, y)
		grid.change(self.loc[0], self.loc[1])
	
	def move(self) :
		self.next_heading()
		self.grid.change(self.loc[0], self.loc[1])
		x = self.loc[0] + self.heading[0]
		y = self.loc[1] + self.heading[1]
		self.loc = (x, y)
		self.grid.change(self.loc[0], self.loc[1])

	def move_to(self, x, y) :
		self.grid.change(self.loc[0], self.loc[1])
		self.loc = (x, y)
		self.grid.change(self.loc[0], self.loc[1])
	
	def next_heading(self) : # Computes h_t+1
		self.new_possible()
		if self.can_move(self.heading) :
			x = random.randint(0, 9)
			if x >= 3 :
				return
		pos = self.possible_headings
		pos.discard(self.heading)
		r = random.randint(0, len(pos) - 1)
		self.heading = list(pos)[r]

	def new_possible(self) :
		self.possible_headings.clear()
		for x in HEADINGS :
			if self.can_move(x) :
				self.possible_headings.add(x)
		
	def can_move(self, heading) :
		x = self.loc[0] + heading[0]
		y = self.loc[1] + heading[1]
		return self.grid.in_bounds(x, y)

	def get_loc(self) :
		return self.loc

	def get_heading(self) :
		return self.heading
