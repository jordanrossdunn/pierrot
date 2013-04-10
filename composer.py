from pcsets.pcset 	import *
from pcsets.pcops 	import *
from pcsets.catalog import *
from pcsets.noteops import *

from mingus.core.value import *

from rhythms 	 import *
from instruments import *

import random

#--------------------------------------------------
# pitch-class set catalog:
catalog = SetCatalog()

#--------------------------------------------------
# pitch-class set helper functions:

def ctvec(pc_set):
	
	common_tone_vector = []
	interval_vector = pc_set.ivec()
	
	for i in range(12):
		if i == 0:
			common_tone_vector.append(len(pc_set))
		elif i < 6:
			common_tone_vector.append(interval_vector[i-1])
		elif i == 6:
			#tritone
			common_tone_vector.append(interval_vector[5]*2)
		else:
			common_tone_vector.append(interval_vector[(12%i)-1])
	return common_tone_vector

def transposition_spectrum(pc_set):

	spectrum = []
	common_tone_vector = ctvec(pc_set)
	max_common_tones = max(common_tone_vector)
	num_common_tones = max_common_tones

	for contrast in range(12):
		transpositions = []
		for index, item in enumerate(common_tone_vector):
			if common_tone_vector[index] == num_common_tones:
				transpositions.append(index)
		if len(transpositions) > 0:
			spectrum.append(transpositions)
		num_common_tones -= 1
		if num_common_tones < 0:
			break

	return spectrum


def select_transposition_by_contrast(pc_set, contrast):

	spectrum = transposition_spectrum(pc_set)
	assert contrast in range(len(spectrum))

	index = random.randint(0, len(spectrum[contrast])-1)
	transpositions = spectrum[contrast]
	selection = transpositions[index]
	return selection


def neighbor_by_contrast(pc_set, contrast):

	spectrum = transposition_spectrum(pc_set)
	assert contrast in range(len(spectrum))

	sequence = []
	sequence.append(pc_set)
	neighbor = pc_set.T(select_transposition_by_contrast(pc_set, contrast))
	sequence.append(neighbor)
	sequence.append(pc_set)

	return sequence


def palindrome_successive_neighbor_by_contrast(pc_set, contrast, depth):

	spectrum = transposition_spectrum(pc_set)
	assert contrast in range(len(spectrum))

	sequence = []

	for cur_depth in range(depth+1):
		if cur_depth == 0:
			reference_set = pc_set
		else:
			reference_set = sub_sequence[1]
		sub_sequence = neighbor_by_contrast(reference_set, contrast)
		sequence.extend(sub_sequence)

	# mirror the sequence:
	mirror_sequence = []
	mirror_sequence.extend(sequence)
	mirror_sequence.pop()
	mirror_sequence.pop()
	mirror_sequence.pop()
	mirror_sequence.reverse()
	
	sequence.extend(mirror_sequence)

	print "palindrome successive neighbor sequence: "
	for index, item in enumerate(sequence):
		if index % 3 == 0: print str(index/3) + ":"
		print str(item)

	return sequence


def cadential_progressive_successive_neighbor(pc_set):

	spectrum = transposition_spectrum(pc_set)
	max_contrast = len(transposition_spectrum(pc_set))

	sequence = []
	
	for cur_contrast in range(max_contrast):
		if cur_contrast == 0:
			reference_set = pc_set
		else:
			reference_set = sub_sequence[1]
		sub_sequence = neighbor_by_contrast(reference_set, cur_contrast)
		sequence.extend(sub_sequence)
	
	sub_sequence = neighbor_by_contrast(pc_set, 0)
	sequence.extend(sub_sequence)
	
	print "cadential progressive neighbor sequence: "
	for index, item in enumerate(sequence):
		if index % 3 == 0: print str(index/3) + ":"
		print str(item)

	return sequence

#--------------------------------------------------

def compose(primary_pc_sets, primary_rhythms, ensemble):

	for index, item in enumerate(primary_pc_sets):
		interval_vector = item.ivec()
		common_tone_vector = ctvec(item)
		print str(interval_vector)
		print str(common_tone_vector)

	#neighbor_by_contrast(primary_pc_sets[0], 2)
	#palindrome_successive_neighbor_by_contrast(primary_pc_sets[0], 2, 2)
	#cadential_progressive_successive_neighbor(primary_pc_sets[0])

	cycle = Rhythm_cycle(primary_rhythms[0])
	# cycle.display()
	cycle.set_outlet_chance(1, 25)
	cycle.set_outlet_chance(2, 25)
	cycle.set_negate_chance(0, 50)
	cycle.display()

	print "next unit: "
	for i in range(100):
		cycle.get_next_unit()
	
	return
	

