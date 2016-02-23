import grid
import bot
import state
import time

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
states = {c.incr() : state.State(x, y, h) for h in bot.HEADINGS for x in
	xrange(size) for y in xrange(size)}

length = len(states)
S_prob = [1.0/length for x in xrange(length)]
T_mat = []

for i in xrange(length) :
	si = states[i]
	si.calc()
	si_t_probs = []
	for j in xrange(length) :
		sj = states[j]
		si_t_probs.append(si.trans_prob(sj))
	T_mat.append(si_t_probs)

def calc_o_vector(obs) :
	O_vector = []
	nothing = False
	if obs[0] is "nothing" :
		nothing = True
	for i in xrange(length) :
		si = states[i]
		O_vector[i:] = [si.emission_prob(obs, nothing)]
	return O_vector

def update(obs) :
	O_vector = calc_o_vector(obs)
	if sum(O_vector) == 0 :
		print "--------------\nWARNING\n-----------------"
	res = []
	for i in xrange(length) :
		res[i:] = [0]
		res[i] += sum([T_mat[j][i] * S_prob[j] * O_vector[i] 
			for j in xrange(length)])
	alpha = sum(res)
	for i in xrange(length) :
		S_prob[i] = res[i] / alpha

def most_likely() :
	max_prob = 0
	index = 0
	for i in xrange(length) :
		p = S_prob[i]
		if p > max_prob :
			max_prob = p
			index = i
	return states[index]

b = g.get_bot()
sensor_grid = grid.Grid(size, size)
ml_grid = grid.Grid(size, size)
accuracy = []
print_grid = True 
print_info = True 
count = 0
for i in xrange(100) :
	obs = g.next()
	update(obs)
	if not obs[0] is "nothing" :
		sensor_grid.set_bot(obs[0][0], obs[0][1])
	ml_state = most_likely()
	if print_grid :
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
	if abs(diff[0]) + abs(diff[1]) == 0 :
		count += 1
	else :
		count = 0
	if count == 3 :
		break
	if print_info :
		info = "Actual" + str(bstate.to_string())
		info += "\tSensor" + str((obs[0], bot.h_to_string(obs[1]))) 
		info += "\tMost likely" + str(ml_state.to_string())
		print info + "\n"
		print "Off by " + str(diff)
	if print_grid :
		time.sleep(1)

s = str(len(accuracy)) + ": "
for x in accuracy :
	s += str(abs(x[0]) + abs(x[1])) + " "
#print "Accuracy as a function of time: "
print s
