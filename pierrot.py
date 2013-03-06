#!/usr/bin/python

from pcsets.pcset 	import *
from pcsets.pcops 	import *
from pcsets.catalog import *
from pcsets.noteops import *

import mingus.core.value as value

from rhythms import *

import string

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

	raw = raw_input("\nEnter pitch-class set " + str(len(primary_pc_sets)) + ": ")
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
		if item == 'A':
			member[index] = 10
		elif item == 'B':
			member[index] = 11
		elif int(item) in range(10):
			member[index] = int(item)

	#put the set into normal form
	temp = PcSet(raw).normal()

	#compensate for bugs in normal()
	if len(str(temp)) == 12:
		temp = (temp.zero()).transpose(member[0])
	elif (len(str(temp)) == 2) and ((member[1]-member[0])%12 == 6):
		temp = temp.transpose(6)

	#check against previous input for equivalent normal and/or prime forms
	equivalent_normal = []
	equivalent_prime = []

	for index, item in enumerate(primary_pc_sets):
		if str(temp) == str(item):
			equivalent_normal.append(index)
		if str(temp.prime()) == str(item.prime()):
			equivalent_prime.append(index)

	resp = "y"
	if int(len(equivalent_normal)) > 0:

		if int(len(equivalent_normal)) == 1:
			print "\nEquivalent normal and prime forms with entry " + str(equivalent_normal)
		else:
			print "\nEquivalent normal form prime forms with entries " + str(equivalent_normal)

		resp = raw_input("\nAllow entry? (y/n): ")

	elif int(len(equivalent_prime)) > 0:

		if int(len(equivalent_prime)) == 1:
			print "\nEquivalent prime form with entry " + str(equivalent_prime)
		else:
			print "\nEquivalent prime form with entries " + str(equivalent_prime)
		
		resp = raw_input("\nAllow entry? (y/n): ")
	
	#add the set to primary_pc_sets[]
	if resp == 'y':
		primary_pc_sets.append(temp)

	#display current primary set collection data
	print "\n" + string.ljust("#", 15) + string.ljust("Normal Form", 25),
	print string.ljust("Prime Form", 25) + string.ljust("Interval Vector", 20)
	print "-" * width
	for index, item in enumerate(primary_pc_sets):
		print string.ljust(str(index), 15) + string.ljust(str(item), 25),
		print string.ljust(str(item.prime()), 25) + string.ljust(str(item.ivec()), 20)
	
	#continue or break?
	again = raw_input("\nEnter another set? (y/n): ")
	while again != "y" and again != "n":
		again = raw_input("\nEnter another set? (y/n): ")
	if again == 'n':
		break
	else:
		continue

##################################################

#get primary rhythms input

relative_durations = get_relative_durations()

options = []
for key, item in relative_durations.iteritems():
	print key
	options.append(key)
options.sort()


print "\n" + string.center(" Primary Rhythms ", width, "~")

while True:

	rhythm = []

	print "\nRhythm " + str(len(primary_rhythms)) + ":"

	while True:

		print "\nBase values:" + str(relative_durations['base'])

		raw = raw_input("\nEnter base value " + str(len(rhythm)) + ": ")
		temp = float(raw)

		
		if(temp in value.base_values):
			print "\nOptions:"
			"""
			for key, item in relative_durations.iteritems():
				print string.ljust(key, 15)
			"""
			for index, item in enumerate(options):
				print string.ljust(str(index), 5) + string.ljust(item, 15)
			raw = raw_input("\nSelect an option: ")

		else:
			print "\nInvalid duration"
			continue

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