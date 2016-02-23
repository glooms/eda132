import grid
import bot
import state

size = 2
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

T_mat = []

for i in xrange(len(states)) :
	si = states[i]
	si.calc()
	si_t_probs = []
	for j in xrange(len(states)) :
		sj = states[j]
		si_t_probs.append(si.trans_prob(sj))
	T_mat.append(si_t_probs)

def calc_o_vector(obs) :
	O_vector = []
	nothing = False
	if obs[0] is "nothing" :
		nothing = True
	for i in xrange(len(states)) :
		si = states[i]
		O_vector[i:] = [si.emission_prob(obs, nothing)]
	return O_vector
#	return states[1].emission_prob(obs, nothing)

print calc_o_vector(("nothing", (1, 1)))
