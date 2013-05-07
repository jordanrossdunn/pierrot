import mingus.core.value
from fractions import Fraction
import random

#--------------------------------------------------
# rhythm values:

def get_values():
	"""Returns a dictionary of note values (relative durations) for use
	within Pierrot."""

	values = 	{'base': [], 'triplet': [], 'quintuplet': [], 'septuplet': [],
				'single-dotted': [], 'double-dotted': [], 'triple-dotted': []}

	values['base'].extend(mingus.core.value.base_values)
	values['triplet'].extend(mingus.core.value.base_triplets)
	values['quintuplet'].extend(mingus.core.value.base_quintuplets)
	values['septuplet'].extend(mingus.core.value.base_septuplets)

	for item in mingus.core.value.base_values:
		values['single-dotted'].append(mingus.core.value.dots(item))
		values['double-dotted'].append(mingus.core.value.dots(item, 2))
		values['triple-dotted'].append(mingus.core.value.dots(item, 3))

	return values

def is_in_values(candidate):
	"""Returns True or False depending on whether the given value is
	found within the dictionary provided by get_values()."""

	for key, item in get_values().iteritems():
		for element in item:
			if candidate == element:
				return True
	return False

def get_value_name(value):
	"""Returns a string representation of the value's common name."""

	for key, item in get_values().iteritems():
		for index, element in enumerate(item):
			if value == element:
				if key == 'base':
					key = ""
				return str(Fraction(1.0/mingus.core.value.base_values[index])) + message + key 

#--------------------------------------------------
# rhythm unit:

class Unit():
	"""A rhythmic Unit class.
	Contains a rhythm value (relative duration) and am is_rest bool to indicate
	whether the unit is intended as either a note or a rest value.
	A list of Unit objects constitutes a rhythm in Pierrot."""

	def __init__(self, value, is_rest):
		#assert is_in_values(value)
		assert isinstance(is_rest, bool)
		self.__value = value
		self.__is_rest = is_rest

	def get_value(self):
		"""Returns the object's value attribute."""
		return self.__value

	def is_rest(self):
		"""Returns the object's is_rest attribute."""
		return self.__is_rest

	def rest_on(self):
		"""Sets the object's is_rest attribute to True."""
		self.__is_rest = True

	def rest_off(self):
		"""Sets the object's is_rest attribute to False."""
		self.__is_rest = False

	def negate(self):
		"""Negates (logically complements) the object's is_rest attribute."""
		return Unit(self.__value, not(self.__is_rest)) 

	def __str__(self):
		if self.__is_rest:
			message = " rest"
		else:
			message = ""
		for key, item in get_values().iteritems():
			for index, element in enumerate(item):
				if self.__value == element:
					if key == 'base':
						key = ""
					else:
						key = " " + key
					return str(Fraction(1.0/mingus.core.value.base_values[index])) + " note" + key + message

def new_unit(message, value):
	"""An interface for instantiating a new Unit object."""

	assert is_in_values(value)
	prompt = str(message) + "Make this a rest? (y/n): "
	resp = raw_input(prompt)
	while resp is not 'y' and resp is not 'n':
		resp = raw_input(prompt)
	if resp is 'y':
		is_rest = True
	else:
		is_rest = False
	return Unit(value, is_rest)

#--------------------------------------------------
# rhythm cycle:

class Rhythm_cycle():
	"""A Rhythm_cycle class.

	This is essentially a loopable/circular rhythm Unit list which can
	be set to stochastically cycle in a variety of ways by optionally setting
	the following at each rhythm index:

		outlet_chance - an opportunity to loop back to the start of the rhythm
		negate_chance - an opportunity to negate a value (convert a rest to a note and vice versa)
		tieVal_chance - an opportunity to tie a value with that at the following index

	If these are not set or set to zero the rhythm will cycle without variation.

	Note: The constructor takes a rhythm (a list of Unit objects)."""

	def __init__(self, rhythm):
		assert isinstance(rhythm[0], Unit)
		self.__rhythm = rhythm
		self.__index = 0
		self.__count = len(rhythm)
		self.__outlet_chance = []
		self.__negate_chance = []
		self.__tieVal_chance = []
		for i in range(self.__count):
			self.__outlet_chance.append(0)
			self.__negate_chance.append(0)
			self.__tieVal_chance.append(0)

	def get_index(self):
		"""Returns the current index/position in the cycle's rhythm attribute"""
		return self.__index

	def __len__(self):
		return self.__count

	def __advance_index(self):
		self.__index += 1
		if self.__index not in range(self.__count):
			self.__index = 0

	def __is_safe_outlet(self, position):
		value = self.__rhythm[position].get_value()
		values = get_values()
		previous_safe_position = 0

		if position == 0:
			return True
		elif value in values['triplet']:
			for i in range(1, position+1):
				if position-i == 0 or self.__rhythm[position-i].get_value() != value:
					previous_safe_position = position-i
					break
			if (position-previous_safe_position)%3 != 1: return False
		elif value in values['quintuplet']:
			for i in range(1, position+1):
				if position-i == 0 or self.__rhythm[position-i].get_value() != value:
					previous_safe_position = position-i
					break
			if (position-previous_safe_position)%5 != 1: return False
		elif value in values['septuplet']:
			for i in range(1, position+1):
				if position-i == 0 or self.__rhythm[position-i].get_value() != value:
					previous_safe_position = position-i
					break
			if (position-previous_safe_position)%7 != 1: return False
		return True

	def set_outlet_chance(self, position, chance):
		"""Sets the outlet_chance at the given position.
		Takes a position (a valid index in the Rhythm_cycle's rhythm) and
		a chance (a float from 0-100)."""

		assert position in range(self.__count) 
		assert chance >= 0 and chance <= 100

		values = get_values()
		if self.__is_safe_outlet(position):
			self.__outlet_chance[position] = chance

	def set_negate_chance(self, position, chance):
		"""Sets the negate_chance at the given position.
		Takes a position (a valid index in the Rhythm_cycle's rhythm) and
		a chance (a float from 0-100)."""

		assert position in range(self.__count) 
		assert chance >= 0 and chance <= 100

		self.__negate_chance[position] = chance

	def set_tieVal_chance(self, position, chance):
		"""Sets the tieVal_chance at the given position.
		Takes a position (a valid index in the Rhythm_cycle's rhythm) and
		a chance (a float from 0-100)."""

		assert position in range(self.__count) 
		assert chance >= 0 and chance <= 100

		self.__tieVal_chance[position] = chance

	def get_next_unit(self):
		"""Stochastically returns the next Unit in the cycle according to
		the object's outlet_chance, negate_chance, and tieVal_chance values."""

		next_unit = self.__rhythm[self.__index]

		if (random.random() * 100) <= self.__outlet_chance[self.__index]:
			self.__index = 0
			next_unit = self.__rhythm[self.__index]

		if (random.random() * 100) <= self.__negate_chance[self.__index]:
			next_unit = next_unit.negate()

		if ((random.random() * 100) <= self.__tieVal_chance[self.__index]):
			value = next_unit.get_value()
			self.__advance_index()
			value = mingus.core.value.add(value, next_unit.get_value())
			next_unit = Unit(value, next_unit.is_rest())

		#print "next: (index = " + str(self.__index) + ") " + str(next_unit.get_value())

		self.__advance_index()

		return next_unit

	def display(self):
		"""Prints a display of the Rythm_cycle."""

		for index, unit in enumerate(self.__rhythm):
			print "Unit " + str(index+1) + ":"
			print "note/rest value: " + str(unit.get_value())
			print "value is rest: " + str(unit.is_rest())
			print "outlet chance: " + str(self.__outlet_chance[index]) + "%"
			print "negate chance: " + str(self.__negate_chance[index]) + "%"
			print "tieVal chance: " + str(self.__tieVal_chance[index]) + "%"

