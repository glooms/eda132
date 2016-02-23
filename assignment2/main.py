import grid
import bot
import state
import time
import sys

# This file contains both the main method and some functions and loops
# which are the implementation of tracking with Hidden Markov Models

size = 10
g = grid.Grid(size, size)
state.g = g

class Counter :
	def __init__(self) :
		self.c = 0
	
	def incr(self) :
		t = self.c
		self.c += 1
		return t
c = Counter()
# Interesting stuff starts here!

# 'states' is a dictionary mapping a number
# from 0 to 4 * size * size to a state
# this variable is used throughout the program to generate the T matrix,
# O diagonal matrix (here represented as a vector and 
# the probability matrix

states = {c.incr() : state.State(x, y, h) for h in bot.HEADINGS for x in
	xrange(size) for y in xrange(size)}
length = len(states) # How many states there are
# 'S_prob' is initialized a vector with uniform
# distribution over all states. It represents the probability of ending
# up in each state at a step in time, (here step = 0 hence any state).
S_prob = [1.0/length for x in xrange(length)] 
# 'T_mat" is the matrix T, the transition matrix
T_mat = []

# This loop initializes 'T_mat'
for i in xrange(length) :
	si = states[i]
	si.calc()
	si_t_probs = [] # A row in 'T_mat'
	for j in xrange(length) :
		sj = states[j]
		# Probability of going from state x_i to x_j
		si_t_probs.append(si.trans_prob(sj))
	T_mat.append(si_t_probs)

# This function calculates a O_vector, used instead of a diagonal
# matrix, given an observation.
def calc_o_vector(obs) :
	O_vector = []
	nothing = False
	if obs[0] is "nothing" :
		nothing = True
	for i in xrange(length) :
		si = states[i]
		O_vector[i:] = [si.emission_prob(obs, nothing)]
	return O_vector

# This is where the action happens.
# This function updates the 'S_prop' matrix representing the state
# probabilities.
# This takes the O_vector for the latest observation, the transpose of
# the tranpose matrix (T_mat with i and j flipped) and the probability
# matrix S_prob. Combines them into the temporary 'res' vector.
# Then it calculates the alpha by summing the 'res' vector to compute
# the new S_prob vector.
def update(obs) :
	O_vector = calc_o_vector(obs)
	res = []
	for i in xrange(length) :
		res[i:] = [0]
		res[i] += sum([O_vector[i] * T_mat[j][i] * S_prob[j]
			for j in xrange(length)])
	alpha = sum(res)
	for i in xrange(length) :
		S_prob[i] = res[i] / alpha

# Computes the most likely state at this point in time by finding the
# state with the highest prob in the S_prob vector.

def most_likely() :
	max_prob = 0
	index = 0
	for i in xrange(length) :
		p = S_prob[i]
		if p > max_prob :
			max_prob = p
			index = i
	return states[index]

# This is the main method

def main(argv) :
	if len(argv) < 0 or len(argv) > 4 :
		print "Inadequate number of parameters, view README"
		return	
	b = g.get_bot()
	sensor_grid = grid.Grid(size, size) # Grid for displaying noisy readings
	ml_grid = grid.Grid(size, size) # Grid for displaying most likely pos
	accuracy = [] # At each step, how far away is the most likely state
	steps = 15 # How many steps the robot should take
	print_info = False # Flag for info
	print_grid = False  # Flag for grid printing
	time_per_step = 0.0
	if len(argv) >= 1 :
		steps = int(argv[0])
	if len(argv) >= 2 :
		print_info = (int(argv[1]) != 0)
	if len(argv) >= 3 :
		print_grid = (int(argv[2]) != 0)
	if len(argv) >= 4 :
		time_per_step = float(argv[3])
	count = 0
	for i in xrange(steps) :
		obs = g.next() # Latest observation
		update(obs)
		if not obs[0] is "nothing" : # Nothing handling
			sensor_grid.set_bot(obs[0][0], obs[0][1])
		ml_state = most_likely()
		if print_grid : # This prints three parallell grids
			ml_grid.set_bot(ml_state.get_x(), ml_state.get_y())
			grid_string = g.to_string().split("\n")
			sensor_string = sensor_grid.to_string().split("\n")
			ml_string = ml_grid.to_string().split("\n")
			for j in xrange(len(grid_string)) :
				print (grid_string[j] + sensor_string[j]
			 		+ ml_string[j])
		bstate = b.to_state()
		diff = bstate.diff(ml_state)
		accuracy.append(diff)
		if print_info :
			info = "Actual" + str(bstate.to_string())
			info += "\tSensor"
			info += str((obs[0], bot.h_to_string(obs[1]))) 
			info += "\tMost likely" + str(ml_state.to_string())
			print info + "\n"
			print "Off by " + str(diff)
		if print_grid :
			time.sleep(time_per_step)
	s = str(len(accuracy)) + ": "
	for x in accuracy :
		s += str(abs(x[0]) + abs(x[1])) + " "
	print "\nAccuracy as a function of time: "
	print s

if __name__ == "__main__" : 
	main(sys.argv[1:])
