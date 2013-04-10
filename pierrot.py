#!/usr/bin/python

from pcsets.pcset 	import *
#from pcsets.pcops 	import *
#from pcsets.catalog import *
#from pcsets.noteops import *

import mingus.core.value

import string
from fractions import Fraction

from rhythms 	 import *
from instruments import *
from composer	 import *

"""documentatioin/summary"""

#--------------------------------------------------
# materials for the composition:

primary_pc_sets = []	# list of primary pitch-class sets
primary_rhythms = []	# list of primary rhythms
ensemble = []			# list of instruments in the ensemble

print_width = 100	

#--------------------------------------------------
# introduction:

print "\n"
print "=" * print_width
print string.center(" Welcome to Pierrot ", print_width, "|")
print "=" * print_width

print "\nWhat are the materials for the composition?"

#--------------------------------------------------
# pitch-class set input:

print "\n" + string.center(" Primary Pitch-Class Sets ", print_width, "~")

while True:

	raw  = raw_input("\nEnter pitch-class set " + str(len(primary_pc_sets)+1) + ": ")
	temp = str(PcSet(raw))

	# check for valid pitch-class set entry
	if len(str(temp)) < 3:
		print "\nInvalid entry!"
		print "\nPlease enter between 3 and 12 unique pitch-classes for each set."
		continue;

	# split the string of the pitch-class set into an integer array 
	member = []
	for i in range(len(temp)):
		member.append(temp[i])
	for index, item in enumerate(member):
		if   item == 'A':
			member[index] = 10
		elif item == 'B':
			member[index] = 11
		elif int(item) in range(10):
			member[index] = int(item)

	# put the set into normal form
	temp = PcSet(raw).normal()

	# compensate for bugs in normal()
	if   len(str(temp)) == 12:
		temp = (temp.zero()).transpose(member[0])
	elif len(str(temp)) == 2 and (member[1]-member[0])%12 == 6:
		temp = temp.transpose(6)

	# check against previous input for equivalent normal and/or prime forms
	equivalent_normal = []
	equivalent_prime = []

	for index, item in enumerate(primary_pc_sets):
		if str(temp) == str(item):
			equivalent_normal.append(index+1)
		if str(temp.prime()) == str(item.prime()):
			equivalent_prime.append(index+1)

	resp = 'y'
	if int(len(equivalent_normal)) > 0:

		if int(len(equivalent_normal)) == 1:
			print "\nEquivalent normal and prime forms with entry "   + str(equivalent_normal)
		else:
			print "\nEquivalent normal and prime forms with entries " + str(equivalent_normal)

		resp = raw_input("Allow entry? (y/n): ")
		while resp != 'y' and resp != 'n':
			resp = raw_input("Allow entry? (y/n): ")

	elif int(len(equivalent_prime)) > 0:

		if int(len(equivalent_prime)) == 1:
			print "\nEquivalent prime form with entry "   + str(equivalent_prime)
		else:
			print "\nEquivalent prime form with entries " + str(equivalent_prime)
		
		resp = raw_input("Allow entry? (y/n): ")
		while resp != 'y' and resp != 'n':
			resp = raw_input("Allow entry? (y/n): ")
	
	# add the set to primary_pc_sets[]
	if resp == 'y':
		primary_pc_sets.append(temp)

	# display current primary set collection data
	print "\n" + string.ljust("#", 5) + string.ljust("Normal Form", 25),
	print string.ljust("Prime Form", 25) + string.ljust("Interval Vector", 25)
	print "-" * int(print_width)
	for index, item in enumerate(primary_pc_sets):
		print string.ljust(str(index+1), 5) + string.ljust(str(item), 25),
		print string.ljust(str(item.prime()), 25) + string.ljust(str(item.ivec()), 25)
	
	# continue or break?
	again = raw_input("\nEnter another set? (y/n): ")
	while again != 'y' and again != 'n':
		again = raw_input("Enter another set? (y/n): ")
	if again == 'n':
		break
	else:
		continue

#--------------------------------------------------
# rhythm input:

print "\n" + string.center(" Primary Rhythms ", print_width, "~")

actions = 	[
				'Use base value',
				'Make single dotted',
				'Make double dotted',
				'Make triple dotted',
				'Make triplet',
				'Make quintuplet',
				'Make septuplet'
			]

while True:

	rhythm = []

	print "\nRhythm " + str(len(primary_rhythms)+1) + ":"

	while True:

		if len(rhythm) > 0:
			# display rhythm progress
			print "\nRhythm " + str(len(primary_rhythms)+1) + ":"
			print "-" * int(print_width)
			for item in rhythm[:-1]:
				print str(item) + ",",
			print str(rhythm[-1])

		# select a base value
		print "\n" + string.ljust("#", 5) + string.ljust("Value", 15)
		print "-" * int(print_width/3)
		for index, item in enumerate(mingus.core.value.base_values):
			value_as_ratio = str(Fraction(1.0/item))
			print string.ljust(str(index+1), 5) + string.ljust(value_as_ratio, 15)

		index = raw_input("\nSelect base note value " + str(len(rhythm)+1) + ": ")
		if (index.isdigit()) and (int(index)-1 in range(len(mingus.core.value.base_values))):
			value = mingus.core.value.base_values[int(index)-1]
		else:
			print "\nInvalid selection."
			continue
		
		# select an action
		base_index = mingus.core.value.base_values.index(value)
		print "\n" + string.ljust("#", 5) + string.ljust("Action", 15)
		print "-" * int(print_width/3)
		for index, item in enumerate(actions):
			print string.ljust(str(index+1), 5) + string.ljust(item, 15) 
		
		action = raw_input("\nSelect an action: ")
		while (not action.isdigit()) or (int(action)-1 not in range(len(actions))):
			action = raw_input("Select an action: ")
		action = int(action)-1

		print ""
		# option actions
		if   action == 0:
			# base value
			rhythm.append(new_unit('', value))
		elif action == 1:
			# single dotted
			rhythm.append(new_unit('', mingus.core.value.dots(value)))
		elif action == 2:
			# double dotted
			rhythm.append(new_unit('', mingus.core.value.dots(value, 2)))
		elif action == 3:
			# triple dotted
			rhythm.append(new_unit('', mingus.core.value.dots(value, 3)))
		elif action == 4:
			# triplet
			for count in range(3):
				part = str(count+1) + "/3: "
				rhythm.append(new_unit(part, mingus.core.value.base_triplets[base_index]))
		elif action == 5:
			# quintuplet
			for count in range(5):
				part = str(count+1) + "/5: "
				rhythm.append(new_unit(part, mingus.core.value.base_quintuplets[base_index]))
		elif action == 6:
			# septuplet
			for count in range(7):
				part = str(count+1) + "/7: "
				rhythm.append(new_unit(part, mingus.core.value.base_septuplets[base_index]))

		# continue or break?
		again = raw_input("\nEnter another note value? (y/n): ")
		while again != "y" and again != "n":
			again = raw_input("Enter another note value? (y/n): ")

		if again == 'n':
			# rhythm complete
			primary_rhythms.append(rhythm)
			rhythm = []

			# display primary_rhythms
			for index, primary_rhythm in enumerate(primary_rhythms):
				print "\nPrimary Rhythm " + str(index+1) + ":"
				print "-" * int(print_width)
				for item in primary_rhythm[:-1]:
					print str(item) + ",",
				print str(primary_rhythm[-1])
			break
		else:
			continue

	# continue or break?
	again = raw_input("\nEnter another rhythm? (y/n): ")
	while again != "y" and again != "n":
		again = raw_input("Enter another rhythm? (y/n): ")
	if again == 'n':
		break
	else:
		continue

#--------------------------------------------------
# instrumentation input:

print "\n" + string.center(" Instrumentation ", print_width, "~")

while True:

	key  = []
	keys = []

	# select instrument category
	print "\n" + string.ljust("#", 5) + string.ljust("Category", 15)
	print "-" * int(print_width/3)
	for index, title in enumerate(get_instrument_categories()):
		print string.ljust(str(index+1), 5) + string.ljust(title, 15)
		keys.append(title)

	selection = raw_input("\nSelect a category: ")
	while (not selection.isdigit()) or (int(selection)-1 not in range(len(get_instrument_categories()))):
		selection = raw_input("Select a category: ")
	key.append(keys[int(selection)-1])
	category = instruments[key[0]]

	keys = []

	# select instrument family
	print "\n" + string.ljust("#", 5) + string.ljust("Family", 15)
	print "-" * int(print_width/3)
	for index, family in enumerate(get_instrument_families(category)):
		print string.ljust(str(index+1), 5) + string.ljust(family, 15)
		keys.append(family)

	selection = raw_input("\nSelect a family: ")
	while (not selection.isdigit()) or (int(selection)-1 not in range(len(get_instrument_families(category)))):
		selection = raw_input("Select a family: ")
	key.append(keys[int(selection)-1])
	family = instruments[key[0]][key[1]]

	print "\n" + str(key[0]) + ":\n"
	print_instrument_family(family)

	# select instrument
	selection = raw_input("\nSelect an instrument: ")
	while (not selection.isdigit()) or (int(selection)-1 not in range(len(family))):
		selection = raw_input("Select an instrument: ")
	selection = int(selection)-1

	instrument = family[selection]

	ensemble.append(instrument)

	# display ensemble
	print "\nEnsemble:\n"
	print string.ljust('#', 5) + string.ljust('Name', 20) + string.ljust('Key', 10) + string.ljust('Range', 15)
	print '-' * 50
	for index, instr in enumerate(ensemble):
		print string.ljust(str(index+1), 5) + string.ljust(instr.name, 20) + string.ljust(instr.key, 10) + string.ljust(str(instr.range), 15)

	#again = raw_input("\nAdd another instrument? (y/n): ")
	break

#--------------------------------------------------
# composition parameter input:

#--------------------------------------------------
# compose and generate midi file:

print("\n")
compose(primary_pc_sets, primary_rhythms, ensemble)
