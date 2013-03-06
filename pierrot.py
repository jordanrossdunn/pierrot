#!/usr/bin/python

from pcsets.pcset 	import *
from pcsets.pcops 	import *
from pcsets.catalog import *
from pcsets.noteops import *

import mingus.core.value as value

from rhythms import *

import string
from fractions import Fraction

#def main():
"""documentatioin/summary"""

#materials for the composition:
primary_pc_sets = []	#list of primary pitch-class sets
primary_rhythms = []	#list of primary rhythms
ensemble = []			#list of instruments in the ensemble
catalog = SetCatalog() 	#the catalog of all pitch-class sets

width = 100	#print width	

##################################################

print "\n"
print "=" * width
print string.center(" Welcome to Pierrot ", width, "|")
#print "\n"
print "~" * width

print "\nWhat are the musical materials for the composition?"

##################################################

#get primary pitch-class set input

print "\n" + string.center(" Primary Pitch-Class Sets ", width, "~")

while True:

	raw  = raw_input("\nEnter pitch-class set " + str(len(primary_pc_sets)) + ": ")
	temp = str(PcSet(raw))

	#check for valid pitch-class set entry
	if len(str(temp)) < 3:
		print "\nInvalid entry!"
		print "\nPlease enter between 3 and 12 unique pitch-classes for each set."
		continue;

	#split the string of the pitch-class set into an integer array 
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

	#put the set into normal form
	temp = PcSet(raw).normal()

	#compensate for bugs in normal()
	if   len(str(temp)) == 12:
		temp = (temp.zero()).transpose(member[0])
	elif len(str(temp)) == 2 and (member[1]-member[0])%12 == 6:
		temp = temp.transpose(6)

	#check against previous input for equivalent normal and/or prime forms
	equivalent_normal = []
	equivalent_prime = []

	for index, item in enumerate(primary_pc_sets):
		if str(temp) == str(item):
			equivalent_normal.append(index)
		if str(temp.prime()) == str(item.prime()):
			equivalent_prime.append(index)

	resp = 'y'
	if int(len(equivalent_normal)) > 0:

		if int(len(equivalent_normal)) == 1:
			print "\nEquivalent normal and prime forms with entry "   + str(equivalent_normal)
		else:
			print "\nEquivalent normal and prime forms with entries " + str(equivalent_normal)

		resp = raw_input("\nAllow entry? (y/n): ")

	elif int(len(equivalent_prime)) > 0:

		if int(len(equivalent_prime)) == 1:
			print "\nEquivalent prime form with entry "   + str(equivalent_prime)
		else:
			print "\nEquivalent prime form with entries " + str(equivalent_prime)
		
		resp = raw_input("\nAllow entry? (y/n): ")
	
	#add the set to primary_pc_sets[]
	if resp == 'y':
		primary_pc_sets.append(temp)

	#display current primary set collection data
	print "\n" + string.ljust("#", 5) + string.ljust("Normal Form", 25),
	print string.ljust("Prime Form", 25) + string.ljust("Interval Vector", 25)
	print "-" * int(width)
	for index, item in enumerate(primary_pc_sets):
		print string.ljust(str(index), 5) + string.ljust(str(item), 25),
		print string.ljust(str(item.prime()), 25) + string.ljust(str(item.ivec()), 25)
	
	#continue or break?
	again = raw_input("\nEnter another set? (y/n): ")
	while again != 'y' and again != 'n':
		again = raw_input("\nEnter another set? (y/n): ")
	if again == 'n':
		break
	else:
		continue

##################################################

#get primary rhythms input

print "\n" + string.center(" Primary Rhythms ", width, "~")

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

	print "\nRhythm " + str(len(primary_rhythms)) + ":"

	while True:

		#select a base value
		print "\nBase note values: "
		print "\n" + string.ljust("#", 5) + string.ljust("Value", 15)
		print "-" * int(width)
		for index, item in enumerate(value.base_values):
			value_as_ratio = str(Fraction(1.0/item))
			print string.ljust(str(index), 5) + string.ljust(value_as_ratio, 15)

		index = raw_input("\nSelect value " + str(len(rhythm)) + ": ")
		if(int(index) in range(len(value.base_values))):
			val = value.base_values[int(index)]
		else:
			print "\nInvalid selection"
			continue
		
		#select an action
		base_index = value.base_values.index(val)
		print "\nActions:"
		print "\n" + string.ljust("#", 5) + string.ljust("Action", 15)
		print "-" * int(width)
		for index, item in enumerate(actions):
			print string.ljust(str(index), 5) + string.ljust(item, 15) 
		
		action = raw_input("\nSelect an action: ")
		while int(action) not in range(len(actions)):
			action = raw_input("\nSelect an action: ")

		#option actions
		if   action == 0:
			#use base value
			print "Action " + str(action)
		elif action == 1:
			#make single dotted
			print "Action " + str(action)
		elif action == 2:
			#make double dotted
			print "Action " + str(action)
		elif action == 3:
			#make triple dotted
			print "Action " + str(action)
		elif action == 4:
			#make triplet
			print "Action " + str(action)
		elif action == 5:
			#make quintuplet
			print "Action " + str(action)
		elif action == 6:
			#make septuplet
			print "Action " + str(action)

		#continue or break?
		again = raw_input("\nEnter another value? (y/n): ")
		while again != "y" and again != "n":
			again = raw_input("\nEnter another value? (y/n): ")
		if again == 'n':
			break
		else:
			continue

	#continue or break?
	again = raw_input("\nEnter another rhythm? (y/n): ")
	while again != "y" and again != "n":
		again = raw_input("\nEnter another rhythm? (y/n): ")
	if again == 'n':
		break
	else:
		continue

##################################################

#print "\nEnsemble/Instrumentation:"
#allow instrument selection from pierrot ensemble presets and custom instrument definition

##################################################

#print "\nDevelopment/Variation"

##################################################

#generate midi file