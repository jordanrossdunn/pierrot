"""A Pierrot example script"""

# insert the parent directory to the path
import sys
sys.path.insert(0, '../')

# import the necessary modules
from composer import *
from mingus.containers.Bar import *

#--------------------------------------------------
"""primary_pc_sets"""

# primary_pc_sets is a list of PcSet objects
primary_pc_sets = list()

pcset1 = PcSet('059')
pcset2 = PcSet('26A')
pcset3 = PcSet('B25')

primary_pc_sets.append(pcset1)
primary_pc_sets.append(pcset2)
primary_pc_sets.append(pcset3)

#--------------------------------------------------
"""primary rhythms"""

# a rhythm is a list of Unit objects
# primary_rhythms is a list of rhythms
primary_rhythms = list()

# to return a dictonary of rhythm values call get_values()
# to return a value's common name call get_value_name(value)

"""Suggestion: Try Creating a rhythm as a sequence of
phrases (sub-rhythms) with outlet_chances positioned/
indexed at the beginning of each phrase."""

# rhythm1:
rhythm1 = list()

rhythm1.append(Unit(dots(4), False))
rhythm1.append(Unit(8, False))
rhythm1.append(Unit(2, False))

rhythm1.append(Unit(4, False))
rhythm1.append(Unit(4, False))
rhythm1.append(Unit(4, False))
rhythm1.append(Unit(2, False))

rhythm1.append(Unit(4, False))
rhythm1.append(Unit(4, False))
rhythm1.append(Unit(2, True))

# rhythm2:
rhythm2 = list()

rhythm2.append(Unit(1, False))
rhythm2.append(Unit(4, False))
rhythm2.append(Unit(8, False))
rhythm2.append(Unit(8, False))
rhythm2.append(Unit(triplet(8), False))
rhythm2.append(Unit(triplet(8), False))
rhythm2.append(Unit(triplet(8), False))

rhythm2.append(Unit(4, False))
rhythm2.append(Unit(8, True))
rhythm2.append(Unit(8, False))
rhythm2.append(Unit(8, False))
rhythm2.append(Unit(8, False))
rhythm2.append(Unit(4, False))

rhythm2.append(Unit(2, False))
rhythm2.append(Unit(4, False))
rhythm2.append(Unit(4, True))


# append rhythms to primary_rhythms:
primary_rhythms.append(rhythm1)
primary_rhythms.append(rhythm2)


#--------------------------------------------------
"""rhythm cycles"""

# rhythm_cycles is a list of Rhythm_cycle objects
rhythm_cycles = list()

# instantiate Rhythm_cycle obects for each rhythm in primary_rhythms and append to rhythm_cycles
for rhythm in primary_rhythms:
	rhythm_cycles.append(Rhythm_cycle(rhythm))

# edit/set rhythm cycles:

# edit cycle for rhythm1 
rhythm_cycles[0].set_negate_chance(6, 33)

rhythm_cycles[0].set_outlet_chance(4, 55)

rhythm_cycles[1].set_tieVal_chance(0, 25)

# edit cycle for rhythm1
rhythm_cycles[1].set_negate_chance(0, 50)
rhythm_cycles[1].set_negate_chance(11, 50)

rhythm_cycles[1].set_outlet_chance(5, 66)

rhythm_cycles[1].set_tieVal_chance(7, 50)

#--------------------------------------------------
"""ensemble (instrumentation)"""

# ensemble is a list of Instrument objects
# note: compose() currently only works for a single MidiInstrument
ensemble = list()

# you may use the instruments dict for a dictionary of MidiInstruments
# or call print_instruments() to print a display of available MidiIntrument

ensemble.append(Piano())

#--------------------------------------------------
# basic parameters

meter = 4, 4
bpm = 220
stability = 75
repeat_chance = 33
repeat_attempts = 4
repeat_loops = 1
repetitions = 0
filename = "example01"
filename = "./output/" + filename + ".mid"

#--------------------------------------------------
# compose

compose(primary_pc_sets, rhythm_cycles, ensemble, meter, bpm, stability, repeat_chance, repeat_attempts, repeat_loops, repetitions, filename)
