import mingus.core.value
from fractions import Fraction

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

class Unit():
	def __init__(self, value, is_rest):
		assert is_in_values(value) and isinstance(is_rest, bool)
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

def new_unit(opening, value):
		assert is_in_values(value)
		prompt = str(opening) + "Make this a rest? (y/n): "
		resp = raw_input(prompt)
		while resp is not 'y' and resp is not 'n':
			resp = raw_input(prompt)
		if resp is 'y':
			is_rest = True
		else:
			is_rest = False
		return Unit(value, is_rest)
