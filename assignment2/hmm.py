import grid
import bot
import time

size = 5
g = grid.Grid(size, size)

class State :	
	def __init__(self, x, y, h) :
		self.loc = (x, y)
		self.h = h
	
	def __init__(self, loc, h) :
		self.loc = loc
		self.h = h

	def get_x(self) :
		return self.loc[0]
	
	def get_y(self) :
		return self.loc[1]

	def get_h(self) :
		return self.h

	def new_state(self, heading) :
		new_x = self.loc[0] + heading[0]
		new_y = self.loc[1] + heading[1]
		return State(new_x, new_y, heading)

	def possible(self, state) :
		return not g.is_wall(state.get_x(), state.get_y())
		

	def get_transitions(self) :
		forward = self.new_state(self.h)
		if self.possible(forward) :
			transitions = self.trans_aux(0.3)
			transitions[forward] = 0.7
			return transitions
		return self.trans_aux(1)

	def trans_aux(self, p) :
		transitions = {}
		state_list = []
		for h in bot.HEADINGS :
			if h is self.h :
				continue
			state = self.new_state(h)
			if self.possible(state) :
				state_list.append(state)
		p /= len(state_list)
		for state in state_list :
			transitions[state] = p
		return transitions

	def get_emissions(self) :
		p_correct = 0.1
		p_s = 0.05
		p_s2 = 0.025
		p_nothing = 0.1
		emissions = {}
		emissions[self] = p_correct
		for e in grid.S :
			x = self.loc[0] + e[0]
			y = self.loc[1] + e[1]
			if g.in_bounds(x, y) :
				state = State((x, y), self.h)
				emissions[state] = p_s
			else :
				p_nothing += p_s
		for e in grid.S_2 :
			x = self.loc[0] + e[0]
			y = self.loc[1] + e[1]
			if g.in_bounds(x, y) :
				state = State((x, y), self.h)
				emissions[state] = p_s2
			else :
				p_nothing += p_s2
		emissions["nothing"] = p_nothing
		return emissions


	def to_string(self) :
		s = "(" + str(self.loc) + ", "
		s += bot.h_to_string(self.h) + ")" 
		return s 

y_t = []
#tracking_grid = grid.Grid(size, size)
for x in xrange(20) :
	g.print_grid()
	o = g.next() # Observation
	y_i = State(o[0], o[1])
#	print(y_i.to_string())
#	if not o[0] is "nothing" :
#		tracking_grid.set_bot(o[0][0], o[0][1])
#	print "\tActual grid\n"
#	print "\n\tTracking grid\n"
#	tracking_grid.print_grid()
#	print g.get_location()
#	print o[0]
	y_t.append(y_i)
#	time.sleep(0.25)

g.print_history()
