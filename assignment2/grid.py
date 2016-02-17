import random

CONST_WALL = 1
CONST_EMPTY = 0
CONST_BOT = 2

def wall(x, y, m, n) :
	if x == 0 or y == 0 or x == m - 1 or y == n - 1 :
		return CONST_WALL
	return CONST_EMPTY

def make_grid(m, n) :
	grid = [[wall(x, y, m, n) for y in xrange(n)] for x in xrange(m)]
	place_bot(grid, m, n)
	return grid

def place_bot(grid, m, n) :
	x = random.randint(1, m - 1)
	y = random.randint(1, n - 1)
	grid[x][y] = CONST_BOT

