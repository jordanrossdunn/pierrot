"""A Pierrot example script"""

# insert the parent directory to the path
import sys
import os
sys.path.insert(0, '../')

# import the necessary modules
from composer import *
from mingus.containers.Bar import *

#--------------------------------------------------
"""primary_pc_sets"""

# primary_pc_sets is a list of PcSet objects
primary_pc_sets = list()

pcset1 = PcSet('016')
pcset2 = PcSet('06')
pcset3 = PcSet('248A')
pcset4 = PcSet('01')

primary_pc_sets.append(pcset1)
primary_pc_sets.append(pcset2)
primary_pc_sets.append(pcset3)
primary_pc_sets.append(pcset4)

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

rhythm1.append(Unit(4, False))
rhythm1.append(Unit(4, False))
rhythm1.append(Unit(4, False))
rhythm1.append(Unit(4, False))
rhythm1.append(Unit(4, False))
rhythm1.append(Unit(4, False))
rhythm1.append(Unit(4, True))

rhythm1.append(Unit(4, False))
rhythm1.append(Unit(4, False))
rhythm1.append(Unit(4, False))
rhythm1.append(Unit(4, False))
rhythm1.append(Unit(4, False))
rhythm1.append(Unit(4, False))
rhythm1.append(Unit(4, True))
rhythm1.append(Unit(4, True))
rhythm1.append(Unit(4, True))

# rhythm2:
rhythm2 = list()

rhythm2.append(Unit(1, False))

rhythm2.append(Unit(4, False))
rhythm2.append(Unit(dots(2), True))


# rhythm3:
rhythm3 = list()

rhythm3.append(Unit(16, False))
rhythm3.append(Unit(16, False))
rhythm3.append(Unit(8, True))
rhythm1.append(Unit(4, True))
rhythm1.append(Unit(4, True))
rhythm1.append(Unit(4, True))

rhythm3.append(Unit(1, False))


# append rhythms to primary_rhythms:
primary_rhythms.append(rhythm1)
primary_rhythms.append(rhythm2)
primary_rhythms.append(rhythm3)


#--------------------------------------------------
"""rhythm cycles"""

# rhythm_cycles is a list of Rhythm_cycle objects
rhythm_cycles = list()

# instantiate Rhythm_cycle obects for each rhythm in primary_rhythms and append to rhythm_cycles
for rhythm in primary_rhythms:
	rhythm_cycles.append(Rhythm_cycle(rhythm))

# edit/set rhythm cycles:

# edit cycle for rhythm1 
rhythm_cycles[0].set_negate_chance(14, 50)

rhythm_cycles[0].set_outlet_chance(7, 33)

# edit cycle for rhythm2
rhythm_cycles[1].set_negate_chance(0, 20)

rhythm_cycles[1].set_outlet_chance(1, 66)

# edit cycle for rhythm3

rhythm_cycles[2].set_outlet_chance(2, 10)
rhythm_cycles[2].set_outlet_chance(3, 25)

rhythm_cycles[2].set_tieVal_chance(0, 33)
rhythm_cycles[2].set_tieVal_chance(1, 33)

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
bpm = 120
stability = 75
repeat_chance = 20
repeat_attempts = 1
repeat_loops = 0
repetitions = 0
filename = "example02"
filename = "./output/" + filename + ".mid"
if not os.path.exists("./output"):
    os.makedirs("./output")

#--------------------------------------------------
# compose

compose(primary_pc_sets, rhythm_cycles, ensemble, meter, bpm, stability, repeat_chance, repeat_attempts, repeat_loops, repetitions, filename)
