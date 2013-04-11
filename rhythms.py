import mingus.core.value
from fractions import Fraction
import random

#--------------------------------------------------
# rhythm values:

def get_values():

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

	for key, item in get_values().iteritems():
		for element in item:
			if candidate == element:
				return True
	return False

def get_value_name(value):

	for key, item in get_values().iteritems():
		for index, element in enumerate(item):
			if value == element:
				if key == 'base':
					key = ""
				return str(Fraction(1.0/mingus.core.value.base_values[index])) + message + key 

#--------------------------------------------------
# rhythm unit:

class Unit():

	def __init__(self, value, is_rest):
		assert is_in_values(value)
		assert isinstance(is_rest, bool)
		self.__value = value
		self.__is_rest = is_rest

	def get_value(self):
		return self.__value

	def is_rest(self):
		return self.__is_rest

	def rest_on(self):
		self.__is_rest = True

	def rest_off(self):
		self.__is_rest = False

	def negate(self):
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
		return self.__index

	def __advance_index(self):
		self.__index += 1
		if self.__index not in range(self.__count):
			self.__index = 0

	def get_next_unit(self):
		if (random.random() * 100) <= self.__outlet_chance[self.__index]:
			self.__index = 0

		next_unit = self.__rhythm[self.__index]

		if (random.random() * 100) <= self.__negate_chance[self.__index]:
			next_unit = next_unit.negate()

		if ((random.random() * 100) <= self.__tieVal_chance[self.__index]) and not next_unit.is_rest():
			value = next_unit.get_value()
			self.__advance_index()
			value = mingus.core.value.add(value, next_unit.get_value())
			next_unit = Unit(value, False)

		print "next: (index = " + str(self.__index) + ") " + str(next_unit)

		self.__advance_index()

		return next_unit

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
		assert position in range(self.__count) 
		assert chance >= 0 and chance <= 100
		values = get_values()
		if self.__is_safe_outlet(position):
			self.__outlet_chance[position] = chance

	def set_negate_chance(self, position, chance):
		assert position in range(self.__count) 
		assert chance >= 0 and chance <= 100
		self.__negate_chance[position] = chance

	def set_tieVal_chance(self, position, chance):
		assert position in range(self.__count) 
		assert chance >= 0 and chance <= 100
		self.__tieVal_chance[position] = chance

	def display(self):
		for index, unit in enumerate(self.__rhythm):
			print "note/rest value: " + str(unit.get_value())
			print "value is rest: " + str(unit.is_rest())
			print "outlet chance: " + str(self.__outlet_chance[index]) + "%"
			print "negate chance: " + str(self.__negate_chance[index]) + "%"
			print "tieVal chance: " + str(self.__tieVal_chance[index]) + "%"

