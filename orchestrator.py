from pc_sequence import *
from instruments import *

from pcsets.noteops import *
#from mingus.core.notes import *
from mingus.containers.Note import Note

global_octave = False #used to control melodic linearity/angularity

class Orchestrator():
	"""An Orchestrator class.
	Takes a Pc_sequence, an Instrument, and a stability level (an
	int from 0-100) to control both the degree of melodic linearity/
	angularity and orchestrates the Pc_sequence to fit within the range
	of the instrument and the likelihood of a pitch to fall between
	the general extreme upper and lower range of the given Instrument."""

	recursion_count = 0

	def __init__(self, pc_sequence, instrument, stability):
		assert isinstance(pc_sequence, Pc_sequence)
		assert isinstance(instrument, Instrument)
		assert isinstance(stability, int) or isinstance(stability, float)
		assert stability >= 0 and stability <= 100

		self.pc_sequence = pc_sequence
		self.instrument = instrument
		self.stability = stability

		self.octave_lower = self.instrument.range[0].octave
		self.octave_upper = self.instrument.range[1].octave

		self.prev_note = False
		self.prev_octave = False
	
	def __next_octave(self):
		global global_octave

		if not global_octave:
			if random.random()*100 >= self.stability:
				# keep initial octave out of lower and upper extreme registers
				quarter_range = ((self.octave_upper-self.octave_lower)/4)
				global_octave = self.prev_octave = random.randint(self.octave_lower+quarter_range, self.octave_upper-quarter_range)
			else:
				global_octave = self.prev_octave = random.randint(self.octave_lower, self.octave_upper)
		elif not self.prev_octave:
			self.prev_octave = global_octave
		elif random.random()*100 >= self.stability:
			global_octave = self.prev_octave = random.randint(self.octave_lower, self.octave_upper)
		
		# return
		if self.prev_octave in range(self.octave_lower, self.octave_upper+1):
			return self.prev_octave
		elif recursion_count < 10:
			recursion_count += 1
			self.prev_octave = __next_octave(self)
		else:
			recursion_count = 0
			global_octave = self.prev_octave = random.randint(self.octave_lower, self.octave_upper)
			return self.prev_octave

	def next(self):
		"""Determines and returns the next Note taking the previous
		Note and stability level into account."""

		assert not self.pc_sequence.completed()

		next = []
		next.append(self.pc_sequence.next())
		note = Note()

		if self.prev_note:
			note = Note(notes(next), self.__next_octave())
			if random.random()*100 >= self.stability:
				while not self.instrument.note_in_range(note) or abs((int(note)-int(self.prev_note))) > 12:
					note = Note(notes(next), self.__next_octave())
			else:
				while not self.instrument.note_in_range(note):
					note = Note(notes(next), self.__next_octave())
		else:
			note = Note(notes(next), self.__next_octave())
			while not self.instrument.note_in_range(note):
				note = Note(notes(next), self.__next_octave())
		
		self.prev_note = note

		return note

	def completed(self):
		"""Returns True if/when the Orchestrator object's Pc_sequence
		has been completed (iterated through) and False otherwise.""" 
		return self.pc_sequence.completed()
