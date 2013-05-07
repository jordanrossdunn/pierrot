#!/usr/bin/python

from pcsets.pcset 	import *
#from pcsets.pcops 	import *
#from pcsets.catalog import *
#from pcsets.noteops import *

import mingus.core.value

import string
from fractions import Fraction
import os

from rhythms 	 import *
from instruments import *
from composer	 import *

"""
A script providing a user interface to Pierrot for creating compositions.
Output is saved to the pierrot/output subdirectory.

Alternatively, the composition tools, the same functions and classes used
indirectly through the user interface, may be used directly by writing one's
own script; example scripts are provided in the pierrot/examples subdirectory.

Compositions are generated using stochastic processes in conjunction with
materials and parameters provided by the user.

Pierrot makes use of and is dependent upon installation of the following Python packages:

	1. mingus (https://code.google.com/p/mingus/)
	2. pcsets (https://code.google.com/p/pcsets/)

Note: tar.gz files of these packages are provided.

Thanks are duely given to the developers of and contributors to these packages.
"""

print_width = 100

#--------------------------------------------------
# materials for the composition:

primary_pc_sets = list()	# list of primary pitch-class sets
primary_rhythms = list()	# list of primary rhythms
ensemble 		= list()	# list of instruments in the ensemble
	
#--------------------------------------------------
# introduction:

os.system(['clear', 'cls'][os.name == 'nt'])

print "=" * print_width
print string.center(" Welcome to Pierrot ", print_width, "|")
print "=" * print_width

print "\nPierrot is an stochastic, post-tonal music composer."
print "\nThis interface will guide you through the process of specifying the materials and other parameters\nfor the composition."
print "\nThe materials/parameters you will be prompted to provide include:\n"
print " 1. Pitch-Class Sets"
print " 2. Rhythms"
print " 2. Rhythm Cycle Settings"
print " 4. Instrumentation"
print " 5. Basic Parameters (meter, bpm, stability, and a variety repetition parameters)"
print " 6. Output Filename"

resp = ''
while resp != 'y' and resp != 'n':
	resp  = raw_input("\nProceed? (y/n): ")
if resp == 'n': quit()

#--------------------------------------------------
# pitch-class set input:

os.system(['clear', 'cls'][os.name == 'nt'])

print "\n" + string.center(" Primary Pitch-Class Sets ", print_width, "~")

while True:

	raw  = raw_input("\nEnter pitch-class set " + str(len(primary_pc_sets)+1) + ": ")

	# check for valid characters
	temp = raw
	if temp.strip(string.digits+'AB') != '':
		print "\nInvalid input."
		print "\nInput may contain only digits 0-9 and characters 'A' and 'B'"
		continue

	# instantiate PcSet
	temp = str(PcSet(raw))

	# check for valid pitch-class set entry
	if len(str(temp)) < 3:
		print "\nInvalid entry!"
		print "\nPlease enter between 3 and 12 unique pitch-classes for each set."
		continue;

	# split the string of the pitch-class set into an integer array 
	member = list()
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
	equivalent_normal = list()
	equivalent_prime = list()

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

	os.system(['clear', 'cls'][os.name == 'nt'])
	print "\n" + string.center(" Primary Pitch-Class Sets ", print_width, "~")
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

os.system(['clear', 'cls'][os.name == 'nt'])

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

	rhythm = list()

	#print "\nRhythm " + str(len(primary_rhythms)+1) + ":"

	while True:

		os.system(['clear', 'cls'][os.name == 'nt'])

		# display primary_rhythms
		print "\n" + string.center(" Primary Rhythms ", print_width, "~")
		if len(primary_rhythms) > 0:
			for index, primary_rhythm in enumerate(primary_rhythms):
				print "\nPrimary Rhythm " + str(index+1) + ":"
				print "-" * int(print_width)
				for item in primary_rhythm[:-1]:
					print str(item) + ",",
				print str(primary_rhythm[-1])

		# display rhythm progress
		if len(rhythm) > 0:
			print "\nRhythm " + str(len(primary_rhythms)+1) + ":"
			print "-" * int(print_width)
			for item in rhythm[:-1]:
				print str(item) + ",",
			print str(rhythm[-1])
		else:
			print "\nRhythm " + str(len(primary_rhythms)+1) + ":"
			print "-" * int(print_width)

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
		
		os.system(['clear', 'cls'][os.name == 'nt'])
		# display primary_rhythms
		print "\n" + string.center(" Primary Rhythms ", print_width, "~")
		if len(primary_rhythms) > 0:
			for index, primary_rhythm in enumerate(primary_rhythms):
				print "\nPrimary Rhythm " + str(index+1) + ":"
				print "-" * int(print_width)
				for item in primary_rhythm[:-1]:
					print str(item) + ",",
				print str(primary_rhythm[-1])

		# display rhythm progress
		if len(rhythm) > 0:
			print "\nRhythm " + str(len(primary_rhythms)+1) + ":"
			print "-" * int(print_width)
			for item in rhythm[:-1]:
				print str(item) + ",",
			print str(rhythm[-1])
		else:
			print "\nRhythm " + str(len(primary_rhythms)+1) + ":"
			print "-" * int(print_width)

		value_as_ratio = str(Fraction(1.0/value))
		print "\nSelected base value: " + value_as_ratio + " note"

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
			rhythm = list()

			# display primary_rhythms
			os.system(['clear', 'cls'][os.name == 'nt'])
			print "\n" + string.center(" Primary Rhythms ", print_width, "~")
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
		os.system(['clear', 'cls'][os.name == 'nt'])
		continue

#--------------------------------------------------
# rhythm cycle settings input:

# create rhythm cycle for each primary rhythm:
rhythm_cycles = list()
for rhythm in primary_rhythms:
	rhythm_cycles.append(Rhythm_cycle(rhythm))

os.system(['clear', 'cls'][os.name == 'nt'])

print "\n" + string.center(" Rhythm Cycle Settings ", print_width, "~")

# section explanation
print "\nFor each each primary rhythm you can optionally set the following for each rhythm index:\n"
print "outlet chance - an opportunity to loop back to the start of the rhythm"
print "negate chance - an opportunity to negate a value (convert a rest to a note and vice versa)"
print "tieVal chance - an opportunity to tie a value with that of the following index"

choice = raw_input("\nEdit rhythm cycle settings? (y/n): ")
while choice != "y" and choice != "n":
		choice = raw_input("Edit rhythm cycle settings? (y/n): ")

if choice == 'y':

	while(True):

		os.system(['clear', 'cls'][os.name == 'nt'])
		print "\n" + string.center(" Rhythm Cycle Settings ", print_width, "~")

		choice = raw_input("\nDisplay primary rhythms? (y/n): ")
		if choice == 'q':
			break
		while choice != "y" and choice != "n":
			choice = raw_input("Display primary rhythms? (y/n): ")

		os.system(['clear', 'cls'][os.name == 'nt'])
		print "\n" + string.center(" Rhythm Cycle Settings ", print_width, "~")

		if choice == 'y':
			# display primary_rhythms
			for index, primary_rhythm in enumerate(primary_rhythms):
				print "\nPrimary Rhythm " + str(index+1) + ":"
				print "-" * int(print_width)
				for item in primary_rhythm[:-1]:
					print str(item) + ",",
				print str(primary_rhythm[-1])

		choice = raw_input("\nDisplay rhythm cycles? (y/n): ")
		if choice == 'q':
			break
		while choice != "y" and choice != "n":
			choice = raw_input("Display rhythm cycles? (y/n): ")

		if choice == 'y':
			# display rhythm cycles
			os.system(['clear', 'cls'][os.name == 'nt'])
			print "\n" + string.center(" Rhythm Cycle Settings ", print_width, "~")
			print "\nRhythm Cycles:"  
			for index, rhythm in enumerate(primary_rhythms):
				print "\nCycle " + str(index+1) + ":"
				rhythm_cycles[-1].display()

		if len(rhythm_cycles) > 1:
			# select rhythm cycles to edit
			print "\n# of rhythm cycles = " + str(len(rhythm_cycles))

			choice = raw_input("\nEnter rhythm cycle (by number) to edit: ")
			if choice == 'q':
				break
			while (not choice.isdigit()) or (int(choice)-1 not in range(len(rhythm_cycles))):
				choice = raw_input("Enter rhythm cycle (by number) to edit: ")
			index = int(choice)-1
		else:
			index = 0

		while(True):

			# display the selected rhythm cycle
			os.system(['clear', 'cls'][os.name == 'nt'])
			print "\n" + string.center(" Rhythm Cycle Settings ", print_width, "~")
			print "\nSelected Rhythm Cycle:"
			print "\nCycle " + str(index+1) + ":" 
			rhythm_cycles[index].display()

			choice = raw_input("\nEnter unit index (by number) to edit: ")
			if choice == 'q':
				break
			while (not choice.isdigit()) or (int(choice)-1 not in range(len(rhythm_cycles[index]))):
				choice = raw_input("Enter unit index (by number) to edit: ")
			position = int(choice)-1

			print "\nEditing Unit " + choice + "\n"

			# display edit options:
			print string.ljust('#', 5) + string.ljust('Edit Option', 20)
			print "-" * int(print_width/3)
			print string.ljust('1', 5) + string.ljust('outlet chance', 20)
			print string.ljust('2', 5) + string.ljust('negate chance', 20)
			print string.ljust('3', 5) + string.ljust('tieVal chance', 20)

			choice = raw_input("\nSelect edit option #: ")
			if choice == 'q':
				break
			while (not choice.isdigit()) or (int(choice) not in range(1, 4)):
				choice = raw_input("Select edit option #: ")

			# display the selected rhythm cycle
			os.system(['clear', 'cls'][os.name == 'nt'])
			print "\n" + string.center(" Rhythm Cycle Settings ", print_width, "~")
			print "\nSelected Rhythm Cycle:"
			print "\nCycle " + str(index+1) + ":" 
			rhythm_cycles[index].display()

			print "\nNote:"
			print "Chance entries must be between 0 and 100 and are considered as a percentage."
			print "A chance of 0 will never happen and a chance of 100 will always happen."

			# edit rhythm cycle attribute at selected position
			if choice == '1':
				# set outlet chance
				chance = raw_input("\nEnter outlet chance for index " + str(position+1) + ": ")
				invalid = False
				try:
					float(chance)
				except ValueError:
					invalid = True
				while invalid or (int(chance) < 0 or int(chance) > 100):
					chance = raw_input("Enter outlet chance for index " + str(position+1) + ": ")
					invalid = False
					try:
						float(chance)
					except ValueError:
						invalid = True
				chance = float(chance)
				rhythm_cycles[index].set_outlet_chance(position, chance)

			elif choice == '2':
				# set negate chance
				chance = raw_input("\nEnter negate chance for index " + str(position+1) + ": ")
				invalid = False
				try:
					float(chance)
				except ValueError:
					invalid = True
				while invalid or (int(chance) < 0 or int(chance) > 100):
					chance = raw_input("Enter negate chance for index " + str(position+1) + ": ")
					invalid = False
					try:
						float(chance)
					except ValueError:
						invalid = True
				chance = float(chance)
				rhythm_cycles[index].set_negate_chance(position, chance)

			elif choice == '3':
				# set tieVal chance
				chance = raw_input("\nEnter tieVal chance for index " + str(position+1) + ": ")
				invalid = False
				try:
					float(chance)
				except ValueError:
					invalid = True
				while invalid or (int(chance) < 0 or int(chance) > 100):
					chance = raw_input("Enter tieVal chance for index " + str(position+1) + ": ")
					invalid = False
					try:
						float(chance)
					except ValueError:
						invalid = True
				chance = float(chance)
				rhythm_cycles[index].set_tieVal_chance(position, chance)

			# display the selected rhythm cycle
			os.system(['clear', 'cls'][os.name == 'nt'])
			print "\n" + string.center(" Rhythm Cycle Settings ", print_width, "~")
			print "\nSelected Rhythm Cycle:"
			print "\nCycle " + str(index+1) + ":" 
			rhythm_cycles[index].display()

			choice = raw_input("\nContinue editing this rhythm cycle? (y/n): ")
			while choice != 'y' and choice != 'n':
				choice = raw_input("Continue editing this rhythm cycle? (y/n): ")
			if choice == 'y':
				continue
			else:
				os.system(['clear', 'cls'][os.name == 'nt'])
				print "\n" + string.center(" Rhythm Cycle Settings ", print_width, "~")
				break

		choice = raw_input("\nEdit another rhythm cycle? (y/n): ")
		while choice != 'y' and choice != 'n':
			choice = raw_input("Edit another rhythm cycle? (y/n): ")
		if choice == 'y':
			continue
		else:
			break


#--------------------------------------------------
# instrumentation input:

os.system(['clear', 'cls'][os.name == 'nt'])

print "\n" + string.center(" Instrumentation ", print_width, "~")

while True:

	key  = list()
	keys = list()

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

	keys = list()

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

	# add selected instrument to ensemble;
	instrument = family[selection]
	ensemble.append(instrument)

	os.system(['clear', 'cls'][os.name == 'nt'])
	# display ensemble
	print "\nEnsemble:\n"
	print string.ljust('#', 5) + string.ljust('Name', 20) + string.ljust('Key', 10) + string.ljust('Range', 15)
	print '-' * 50
	for index, instr in enumerate(ensemble):
		print string.ljust(str(index+1), 5) + string.ljust(instr.name, 20) + string.ljust(instr.key, 10) + string.ljust(str(instr.range), 15)

	#again = raw_input("\nAdd another instrument? (y/n): ")
	break

#--------------------------------------------------
# basic composition parameter input:

os.system(['clear', 'cls'][os.name == 'nt'])
print "\n" + string.center(" Composition Parameters ", print_width, "~")

# meter entry:
print "\nMeter (Time Signature):"
print "\n(beats per measure / beat value)"

beat_count = raw_input("\nEnter beats per measure (1-100): ")
while not beat_count.isdigit() or int(beat_count) not in range(1, 101):
	 beat_count = raw_input("\nEnter beats per measure (1-100): ")

beat_value = raw_input("\nEnter beat value (1, 2, 4, 8, 16, 32): ")
while not beat_value.isdigit() or int(beat_value) not in {1, 2, 4, 8, 16, 32}:
	 beat_value = raw_input("\nEnter beat value (1, 2, 4, 8, 16, 32): ")

meter = int(beat_count), int(beat_value)
print "\nMeter entered: " + str(beat_count) + "/" + str(beat_value) + " - " + str(meter)

os.system(['clear', 'cls'][os.name == 'nt'])
print "\n" + string.center(" Composition Parameters ", print_width, "~")

# bpm entry:
# print tempo marking to bpm guide
print "\n" + string.ljust("Tempo Marking", 15) + string.ljust("bpm", 10)
print "-" * 25
print string.ljust("Grave", 15) 		+ string.ljust("20-40", 10)
print string.ljust("Largo", 15) 		+ string.ljust("40-60", 10)
print string.ljust("Larghetto", 15) 	+ string.ljust("60-66", 10)
print string.ljust("Adagio", 15) 		+ string.ljust("66-76", 10)
print string.ljust("Andante", 15) 		+ string.ljust("76-108", 10)
print string.ljust("Moderato", 15) 		+ string.ljust("108-120", 10)
print string.ljust("Allegro", 15) 		+ string.ljust("120-168", 10)
print string.ljust("Presto", 15) 		+ string.ljust("168-200", 10)
print string.ljust("Prestissimo", 15) 	+ string.ljust("200-208", 10)

bpm_upper_limit = 100000 # arbitrary upper limit

raw = raw_input("\nEnter bmp (beats per minute): ")
while (not raw.isdigit()) or (int(raw) < 0) or (int(raw) > bpm_upper_limit):
	if raw.isdigit() and ((int(raw) < 0) or (int(raw) > bpm_upper_limit)):
		print "Please enter a value between 0 and " + str(bpm_upper_limit)
	raw = raw_input("\nEnter bmp (beats per minute): ")
bpm = int(raw)

os.system(['clear', 'cls'][os.name == 'nt'])
print "\n" + string.center(" Composition Parameters ", print_width, "~")

print """Stability
\nThe stability value controls the likelihood of a melodic leap greater than an octave.
\nThe overall melodic linearity/angularity of the composition is affected by this value."""

raw = raw_input("\nEnter stability value (0-100): ")
while (not raw.isdigit()) or (float(raw) < 0 or float(raw) > 100):
	raw = raw_input("\nEnter stability value [0-100]: ")
stability = int(raw)

os.system(['clear', 'cls'][os.name == 'nt'])
print "\n" + string.center(" Composition Parameters ", print_width, "~")

print """\nRepetition Parameters\n
- 'repeat chance' controls the likelyhood of consecutively repeating a pitch-class.
- 'repeat attempts' controls the number of times this will be consecutively attempted.
- 'repeat loops' is the number of times this process is looped.
- 'repetitions' is the number of times the entire composition will repeat."""

raw = raw_input("\nEnter repeat chance [0-100]: ")
while (not raw.isdigit()) or (float(raw) < 0 or float(raw) > 100):
	raw = raw_input("\nEnter repeat chance [0-100): ")
repeat_chance = float(raw)

raw = raw_input("\nEnter repeat attempts [0-100]: ")
while (not raw.isdigit()) or (int(raw) not in range(0, 101)):
	raw = raw_input("\nEnter repeat attempt [0-100]: ")
repeat_attempts = int(raw)

raw = raw_input("\nEnter repeat loops [0-100]: ")
while (not raw.isdigit()) or (int(raw) not in range(0, 101)):
	raw = raw_input("\nEnter repeat loops [0-100]: ")
repeat_loops = int(raw)

# repeat entry (da capo count):
raw = raw_input("\nEnter # of repetitions: ")
while (not raw.isdigit()) or (int(raw) not in range(0, 101)):
	raw = raw_input("\nEnter # of repetitions: ")
repetitions = int(raw)

#title entry:
#author entry:

#--------------------------------------------------
# compose and generate midi file:

os.system(['clear', 'cls'][os.name == 'nt'])

print "\n" + string.center(" Composition Generation ", print_width, "~")

# filname entry
filename = raw_input("\nEnter filename (the '.mid' file extension will be automatically appended): ")

valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
filename = ''.join(c for c in filename if c in valid_chars)
filename = filename.replace(' ','_')

filename = filename + ".mid"
print "Using filename: " + filename
# direct to pierrot output subdirectory
if not os.path.exists("./output"):
    os.makedirs("./output")
filename = "./output/" + filename
print "\nSaving output to: " + filename

# compose (and generate <filename>.mid file)
compose(primary_pc_sets, rhythm_cycles, ensemble, meter, bpm, stability, repeat_chance, repeat_attempts, repeat_loops, repetitions, filename)

#print "\nCompleted."
#print "\nOutput saved as: " + filename + "\n"

quit()
