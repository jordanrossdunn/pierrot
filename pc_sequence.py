from pcsets.pcset import *

import random

class Pc_sequence():
	"""A Pc_sequence class.
	Takes a PcSet, a float or int for repeat chance, and integers for
	both repeat attempts and repeat loops and creates a randomly ordered
	sequence (list) of pitch classes taking repeat parameters into account.
	Repeat chance controls the likelyhood of consecutively repeating a
	pitch-class, repeat attempts controls the number of times this will be
	consecutively attempted, and repeat loops is the number of times this
	process is looped."""
	
	def __init__(self, pc_set, repeat_chance, repeat_attempts, repeat_loops):
		assert isinstance(pc_set, PcSet)
		assert isinstance(repeat_chance, int) or isinstance(repeat_chance, float)
		assert repeat_chance >= 0 and repeat_chance <= 100
		assert isinstance(repeat_attempts, int)
		assert repeat_attempts in range(0, 101)
		assert isinstance(repeat_loops, int)
		assert repeat_loops in range(0, 101) 

		self.sequence = list()
		#self.sequence.extend(pc_set)

		self.pc_set = pc_set
		self.repeat_chance = repeat_chance
		self.repeat_attempts = repeat_attempts
		self.repeat_loops = repeat_loops

		self.renew()

	def __len__(self):
		return len(self.sequence)

	def reshuffle(self):
		"""Reshuffles the object's sequence attribute."""
		random.shuffle(self.sequence)

	def renew(self):
		"""Renews the object's sequence according to the object's
		pc_set, repeat_chance, and repeat_attempts attributes."""

		self.sequence = list()

		for times in range(self.repeat_loops+1):
			shuffled = list()
			shuffled.extend(self.pc_set)
			random.shuffle(shuffled)
			for index in range(len(shuffled)):
				self.sequence.append(shuffled[index])
				for attempts in range(self.repeat_attempts+1):
					if random.random()*100 <= self.repeat_chance:
						self.sequence.append(shuffled[index])

	def completed(self):
		"""Returns True if/when the object's sequence has been completed
		(iterated through) and False otherwise."""
		return len(self.sequence) == 0

	def next(self):
		"""Pops the next element off of the object's sequence."""
		assert not self.completed()
		return self.sequence.pop(0)