import grid
import bot

class State :
	def __init__(self, x, y, h) :
		self.loc = (x, y)
		self.h = h
	
	def get_x(self) :
		return self.loc[0]
	
	def get_y(self) :
		return self.loc[1]

	def get_h(self) :
		return self.h

	def getID(self) :
		x = self.loc[0]
		y = self.loc[1]
		h = self.h
		s = str(x) + str(y) + str(h[0]) + str(h[1])
		return s 

	def new_state(self, heading) :
		new_x = self.loc[0] + heading[0]
		new_y = self.loc[1] + heading[1]
		return State(new_x, new_y, heading)

	def possible(self, state) :
		return g.in_bounds(state.get_x(), state.get_y())
		

	def trans_prob(self, state) :
		#print self.transitions
		sid = state.getID()
		if sid in self.transitions :
			return self.transitions[sid]
		return 0

	def calc(self) :
		self.calc_transitions()
		self.calc_emissions()

	def calc_transitions(self) :
		forward = self.new_state(self.h)
		if self.possible(forward) :
			transitions = self.trans_aux(0.3)
			transitions[forward.getID()] = 0.7
			self.transitions = transitions
			return
		self.transitions = self.trans_aux(1.0)
		return

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
			transitions[state.getID()] = p
		return transitions

	def calc_emissions(self) :
		p_correct = 0.1
		p_s = 0.05
		p_s2 = 0.025
		p_nothing = 0.1
		self.emissions = {}
		self.emissions[self.getID()] = p_correct
		for e in grid.S :
			x = self.loc[0] + e[0]
			y = self.loc[1] + e[1]
			if g.in_bounds(x, y) :
				state = State(x, y, self.h)
				self.emissions[state.getID()] = p_s
			else :
				p_nothing += p_s
		for e in grid.S_2 :
			x = self.loc[0] + e[0]
			y = self.loc[1] + e[1]
			if g.in_bounds(x, y) :
				state = State(x, y, self.h)
				self.emissions[state.getID()] = p_s2
			else :
				p_nothing += p_s2
		self.emissions["nothing" + str(self.h[0]) +
			str(self.h[0])] = p_nothing

	def emission_prob(self, state, nothing) :
		if nothing :
			sid = state[0]
			sid += str(state[1][0]) + str(state[1][1])
			if sid in self.emissions :
				return self.emissions[sid]
			return 0
		sid = state.getID()
		if sid in self.emissions :
			return self.emissions[sid]
		return 0

	def to_string(self) :
		s = "(" + str(self.loc) + ", "
		s += bot.h_to_string(self.h) + ")" 
		return s 


