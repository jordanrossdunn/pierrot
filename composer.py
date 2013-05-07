from pcsets.pcset 	import *
from pcsets.pcops 	import *
#from pcsets.catalog import *
from pcsets.noteops import *

from mingus.core.value import *
from mingus.core.notes import *
from mingus.containers.Note import Note
from mingus.containers.Bar import *
from mingus.containers.Track import *
from mingus.containers.Composition import *

from mingus.midi.MidiFileOut import *
from mingus.midi import fluidsynth

from rhythms 	  import *
from instruments  import *
#from pc_sequence  import *
from orchestrator import *

from math import floor

import random

#--------------------------------------------------
# pitch-class set catalog:
#catalog = SetCatalog()

#--------------------------------------------------
# composition helper functions:

def ctvec(pc_set):
	"""Returns a list of the number common tones under each transposition
	(from T0-T11) of the given PcSet indexed by transposition level."""

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
	"""Returns a list of lists of transposition levels of the given
	PcSet yielding equal numbers of common tones from max to min.""" 

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
	"""Returns a randomly selected a transposition level from the
	given PcSet's trasposition spectrum at the specified contrast
	level index.
	The contrast level is expected to be within range of the PcSet's
	transposition spectrum."""

	spectrum = transposition_spectrum(pc_set)
	assert contrast in range(len(spectrum))

	index = random.randint(0, len(spectrum[contrast])-1)
	transpositions = spectrum[contrast]
	selection = transpositions[index]
	return selection

def neighbor_by_contrast(pc_set, contrast):
	"""Returns a neighboring sequence of transpositions of the given
	PcSet at the given contrast level.
	The contrast level is expected to be within range of the PcSet's
	transposition spectrum."""

	spectrum = transposition_spectrum(pc_set)
	assert contrast in range(len(spectrum))

	sequence = []
	sequence.append(pc_set)
	neighbor = pc_set.T(select_transposition_by_contrast(pc_set, contrast))
	sequence.append(neighbor)
	sequence.append(pc_set)

	return sequence

def palindrome_successive_neighbor_by_contrast(pc_set, contrast, depth):
	"""Returns a palindromic, successive neighboring sequence of
	transpositions of the given PcSet at the given contrast level
	to the given depth (# of neighboring sequences to midway-point).
	The contrast level is expected to be within range of the PcSet's
	transposition spectrum."""

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

	return sequence

def cadential_progressive_successive_neighbor(pc_set):
	"""Returns a cadential, progressive, successive neighboring sequence
	of increasingly contrasting transpositions of the given PcSet."""

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
	
	return sequence

#--------------------------------------------------

def my_change_note_duration(self, at, to):
	"""Change the note duration at the given index to the given duration."""

	if mingus.core.meter.valid_beat_duration(to):
		diff = 0
		for x in self.bar:
			if diff != 0:
				x[0] -= diff
			if x[0] == at:
				cur = x[1]
				x[1] = to
				diff = 1/cur - 1/to
		return True
	else:
		return False

mingus.containers.Bar.change_note_duration = my_change_note_duration
change_note_duration = my_change_note_duration


#--------------------------------------------------
def compose(primary_pc_sets, rhythm_cycles, ensemble, meter, bpm, stability, repeat_chance, repeat_attempts, repeat_loops, repetitions, filename = 'output.mid'):
	"""
	Generates a post-tonal composition and resultant midi file
	using the given materials (function arguments) in conjunction
	with stochastic processes.
	Takes a list of PcSets, a list of Rythm_cycles, a list of Instruments,
	an integer tuple for meter (time signature), an integer for bpm
	(tempo), a floats for stability and repeat_chance, integers for
	repeat_loops and repetitions, and a string for output filename.
	"""
	
	for pc_set in primary_pc_sets:
		assert isinstance(pc_set, PcSet)
	for rhythm_cycle in rhythm_cycles:
		assert isinstance(rhythm_cycle, Rhythm_cycle)
	for instrument in ensemble:
		assert isinstance(instrument, Instrument)
	assert isinstance(meter, tuple)
	assert isinstance(bpm, int)
	assert isinstance(stability, int) or isinstance(stability, float)
	assert stability >= 0 and stability <= 100
	assert isinstance(repeat_chance, int) or isinstance(repeat_chance, float)
	assert repeat_chance >= 0 and repeat_chance <= 100
	assert isinstance(repeat_attempts, int)
	assert repeat_attempts in range(0, 101)
	assert isinstance(repeat_loops, int)
	assert repeat_loops in range(0, 101)
	assert isinstance(repetitions, int)
	assert repetitions in range(0, 101)
	assert isinstance(filename, str)

	# print parameters:
	print "\nBasic Parameters:\n"
	print "Meter: " + str(meter)
	print "BPM: " + str(bpm)
	print "Repeat chance:" + str(repeat_chance)
	print "Repeat attempts:" + str(repeat_attempts)
	print "Repeat loops:" + str(repeat_loops)
	print "Repetitions: " + str(repetitions)
	print "Output Destination: " + filename

	print "\nPrimary Pitch-Class Sets:"
	for index, item in enumerate(primary_pc_sets):
		interval_vector = item.ivec()
		common_tone_vector = ctvec(item)
		print "\n#" + str(index+1) + ":"
		print "Pitch-Class Set: " + str(item)
		print "Interval Vector: " + str(interval_vector)
		print "Common-Tone Vector: " + str(common_tone_vector)

	print "\nRhythm Cycles:"  
	for index, rhythm in enumerate(rhythm_cycles):
		print "\n#" + str(index+1) + ":"
		rhythm_cycles[-1].display()

	# compose pc_set_progression sections:
	pc_set_progression = list()
	section_length = list()

	# section 1:
	for index, primary_pc_set in enumerate(primary_pc_sets):
		spectrum = transposition_spectrum(primary_pc_set)
		contrast = index
		if contrast not in range(len(spectrum)):
			contrast = len(spectrum)-1
		pc_set_progression.extend(neighbor_by_contrast(primary_pc_set, contrast))
	section_length.append(len(pc_set_progression))

	# section 2:
	for index, primary_pc_set in enumerate(primary_pc_sets):
		spectrum = transposition_spectrum(primary_pc_set)
		contrast = index
		if contrast not in range(len(spectrum)):
			contrast = len(spectrum)-1
		pc_set_progression.extend(palindrome_successive_neighbor_by_contrast(primary_pc_set, contrast, index+1))
	section_length.append(len(pc_set_progression))

	# section 3:
	primary_pc_set = primary_pc_sets[-1]
	spectrum = transposition_spectrum(primary_pc_set)
	contrast = len(spectrum)-1
	pc_set_progression.extend(cadential_progressive_successive_neighbor(primary_pc_set))
	section_length.append(len(pc_set_progression))

	# section 4:
	for index, primary_pc_set in enumerate(reversed(primary_pc_sets)):
		spectrum = transposition_spectrum(primary_pc_set)
		contrast = index
		if contrast not in range(len(spectrum)):
			contrast = len(spectrum)-1
		pc_set_progression.extend(neighbor_by_contrast(primary_pc_set, contrast))
	section_length.append(len(pc_set_progression))

	print "\nSub progression lengths:"
	for item in section_length:
		print str(item)

	print "\nPitch-Class Set Progression:"
	for index, item in enumerate(pc_set_progression):
		print str(index) + ": " + str(item)

	# compose pc_sequence:
	pc_sequence = list()

	print "\nPitch-Class Sequence:"
	for pc_set in pc_set_progression:
		seq = Pc_sequence(pc_set, repeat_chance, repeat_attempts, repeat_loops)
		pc_sequence.append(seq)
		print str(pc_sequence[-1].sequence)

	instrument = ensemble[0]
	track = Track(instrument)
	track.name = instrument.name
	composition = Composition()

	#title = "my title"
	#composition.set_title(title)
	#print composition.title

	#author = "Pierrot"
	#composition.set_author(author)
	#print composition.author

	note = Note()
	track.add_bar(Bar())
	track.bars[-1].set_meter(meter)

	count = 0
	cur_rhythm_cycle = 0
	cur_section = 0

	first_note = False

	for index, item in enumerate(pc_sequence):

		orchestrator = Orchestrator(item, instrument, stability)

		while not orchestrator.completed():

			print "\ncount = " + str(count)
			print "rhythm cycle # " + str(cur_rhythm_cycle)
			print "section # " + str(cur_section)
			print "section length = " + str(section_length[cur_section])

			# select rhythm cycle
			if index == len(pc_sequence)-1:
				cycle = rhythm_cycles[cur_rhythm_cycle]
			else:
				if count == 0:
					cycle = rhythm_cycles[cur_rhythm_cycle]
				elif count % section_length[cur_section] == 0:
					cur_rhythm_cycle += 1
					cur_section += 1
					if cur_rhythm_cycle == len(rhythm_cycles):
						cur_rhythm_cycle = 0
					if cur_section == len(section_length):
						cur_section = 0
					cycle = rhythm_cycles[cur_rhythm_cycle]

			unit = cycle.get_next_unit()

			print "cycle position = " + str(cycle.get_index())
			print "unit value = " + str(unit.get_value())

			if track.bars[-1].is_full():
				track.add_bar(Bar())
				track.bars[-1].set_meter(meter)

			if unit.is_rest():
				print "rest"
				if not track.bars[-1].place_rest(unit.get_value()):
					print "not enough room in bar"
					if track.bars[-1].space_left() == 0:
						print "adding new bar"
						track.add_bar(Bar())
						track.bars[-1].set_meter(meter)
					value_left = track.bars[-1].value_left()
					if track.bars[-1].space_left >= 1.0/unit.get_value():
						print "placing rest"
						track.bars[-1].place_rest(unit.get_value())
					else:
						difference = subtract(unit.get_value(), value_left)
						while difference != 0:
							print "spliting rest across bars"
							track.bars[-1].place_rest(value_left)
							track.add_bar(Bar())
							track.bars[-1].set_meter(meter)
							if space_left >= 1.0/difference:
								track.bars[-1].place_rest(difference)
								break
			else:
				print "note"
				note = orchestrator.next()
				if not first_note:
					first_note = note
				print str(next)
				if not track.bars[-1].place_notes(note, unit.get_value()):
					print "not enough room in bar"
					if track.bars[-1].space_left() != 0:
						value_left = track.bars[-1].value_left()
						print "value left = " + str(value_left)
						cur_beat = track.bars[-1].current_beat
						print "filling in remaining space"
						track.bars[-1].place_notes(note, value_left)

						value_needed = subtract(unit.get_value(), value_left)

						print "adding bars to fit full value"
						track.add_bar(Bar())
						track.bars[-1].set_meter(meter)
						value_bar = track.bars[-1].value_left()

						bars_added = 1
						while 1.0/value_needed > 1.0/value_bar:
							print "adding bar"
							track.add_bar(Bar())
							track.bars[-1].set_meter(meter)
							value_needed = subtract(value_needed, value_bar)
							bars_added+=1

						if not track.bars[-bars_added].place_notes_at(cur_beat, unit.get_value()):
							print "could not fit value"
		count+=1

	note = first_note
	
	composition.add_track(track)

	write_Composition(filename, composition, bpm, repetitions)

	print "\n"
	print repr(composition)

	print "\nCompleted."
	print "\nOutput saved as: " + filename + "\n"

	return
	

