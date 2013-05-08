import mingus.containers.Instrument as Instrument
from mingus.containers.Instrument import MidiInstrument
import mingus.containers.Note as Note
import string

#--------------------------------------------------

# all intruments (by category and family):
instruments = dict()

# instrument categories:
woodwinds = dict()
strings = dict()
percussion = dict()

# instrument families:

# woodwinds:
clarinets = list()
saxophones = list()
flutes = list()

# strings:
violins = list()
plucked_strings = list()

# percussion
pitched_percussion = list()
keyboards = list()

#--------------------------------------------------

def print_instrument_family(family):
	"""Prints a displays of the instruments in the given instrument family."""

	print string.ljust('#', 5) + string.ljust('Name', 20) + string.ljust('Key', 10) + string.ljust('Range', 15)
	print '-' * 50
	for index, instr in enumerate(family):
		print string.ljust(str(index+1), 5) + string.ljust(instr.name, 20) + string.ljust(instr.key, 10) + string.ljust(str(instr.range), 15)

def print_instruments():
	"""Prints a display of all instruments by category and family"""

	for title, category in instruments.iteritems():
		print "\n" + string.center(" " + title + " ", 50, "~")
		for name, family in category.iteritems():
			print "\n" + string.center(" " + name + " ", 50, "-") + "\n"
			print_instrument_family(family)

#--------------------------------------------------

def get_instrument_families(category):
	"""Returns the list of instrument families within the given instrument category"""

	families = list()
	for name, family in category.iteritems():
		families.append(name)
	return families

def get_instrument_categories():
	"""Returns a list of instrument categories"""

	categories = list()
	for title, category in instruments.iteritems():
		categories.append(title)
	return categories

#--------------------------------------------------
# clarinets:

def Clarinet():
	"""Defines and returns a clarinet midi instrument (an instance of MidiInstrument())"""
	
	instr = MidiInstrument()
	instr.name = 'Clarinet'
	instr.key  = 'Bb'
	instr.clef = 'Treble'
	instr.set_range(tuple([Note('D', 3), Note('Bb', 6)]))
	instr.instrument_nr = instr.names.index('Clarinet')
	return instr

def Bass_Clarinet():
	"""Defines and returns a bass clarinet midi instrument (an instance of MidiInstrument())"""

	instr = MidiInstrument()
	instr.name = 'Bass Clarinet'
	instr.key  = 'Bb'
	instr.clef = 'Treble'
	instr.set_range(tuple([Note('Bb', 1), Note('B', 5)]))
	instr.instrument_nr = instr.names.index('Clarinet')
	return instr

clarinets.append(Clarinet())
clarinets.append(Bass_Clarinet())

#--------------------------------------------------
# saxophones:

def Soprano_Saxophone():
	"""Defines and returns a soprano saxophone midi instrument (an instance of MidiInstrument())"""

	instr = MidiInstrument()
	instr.name = 'Soprano Saxophone'
	instr.key  = 'Bb'
	instr.clef = 'Treble'
	instr.set_range(tuple([Note('Ab', 3), Note('E', 6)]))
	instr.instrument_nr = instr.names.index('Soprano Sax')
	return instr

def Alto_Saxophone():
	"""Defines and returns an alto saxophone midi instrument (an instance of MidiInstrument())"""
	
	instr = MidiInstrument()
	instr.name = 'Alto Saxophone'
	instr.key  = 'Eb'
	instr.clef = 'Treble'
	instr.set_range(tuple([Note('Db', 3), Note('A', 5)]))
	instr.instrument_nr = instr.names.index('Alto Sax')
	return instr

def Tenor_Saxophone():
	"""Defines and returns a tenor saxophone midi instrument (an instance of MidiInstrument())"""
	
	instr = MidiInstrument()
	instr.name = 'Tenor Saxophone'
	instr.key  = 'Bb'
	instr.clef = 'Treble'
	instr.set_range(tuple([Note('Ab', 2), Note('E', 5)]))
	instr.instrument_nr = instr.names.index('Tenor Sax')
	return instr

def Baritone_Saxophone():
	"""Defines and returns a baritone saxophone midi instrument (an instance of MidiInstrument())"""
	
	instr = MidiInstrument()
	instr.name = 'Baritone Saxophone'
	instr.key  = 'Eb'
	instr.clef = 'Treble'
	instr.set_range(tuple([Note('C', 2), Note('A', 4)]))
	instr.instrument_nr = instr.names.index('Baritone Sax')
	return instr

saxophones.append(Soprano_Saxophone())
saxophones.append(Alto_Saxophone())
saxophones.append(Tenor_Saxophone())
saxophones.append(Baritone_Saxophone())

#--------------------------------------------------
# flutes:

def Flute():
	"""Defines and returns a flute midi instrument (an instance of MidiInstrument())"""
	
	instr = MidiInstrument()
	instr.name = 'Flute'
	instr.key  = 'C'
	instr.clef = 'Treble'
	instr.set_range(tuple([Note('C', 4), Note('C', 7)]))
	instr.instrument_nr = instr.names.index('Flute')
	return instr

def Alto_Flute():
	"""Defines and returns an alto flute midi instrument (an instance of MidiInstrument())"""

	instr = MidiInstrument()
	instr.name = 'Alto Flute'
	instr.key  = 'G'
	instr.clef = 'Treble'
	instr.set_range(tuple([Note('G', 3), Note('G', 6)]))
	instr.instrument_nr = instr.names.index('Flute')
	return instr

flutes.append(Flute())
flutes.append(Alto_Flute())

#--------------------------------------------------
# violins:

def Violin():
	"""Defines and returns a violin midi instrument (an instance of MidiInstrument())"""

	instr = MidiInstrument()
	instr.name = 'Violin'
	instr.key  = 'C'
	instr.clef = 'Treble'
	instr.set_range(tuple([Note('G', 3), Note('E', 7)]))
	instr.instrument_nr = instr.names.index('Violin')
	return instr

def Viola():
	"""Defines and returns a viola midi instrument (an instance of MidiInstrument())"""
	
	instr = MidiInstrument()
	instr.name = 'Viola'
	instr.key  = 'C'
	instr.clef = 'Alto'
	instr.set_range(tuple([Note('C', 3), Note('A', 7)]))
	instr.instrument_nr = instr.names.index('Viola')
	return instr

def Cello():
	"""Defines and returns a cello midi instrument (an instance of MidiInstrument())"""
	
	instr = MidiInstrument()
	instr.name = 'Cello'
	instr.key  = 'C'
	instr.clef = 'Bass'
	instr.set_range(tuple([Note('C', 2), Note('E', 6)]))
	instr.instrument_nr = instr.names.index('Cello')
	return instr

def Contrabass():
	"""Defines and returns a contrabass midi instrument (an instance of MidiInstrument())"""
	
	instr = MidiInstrument()
	instr.name = 'Contrabass'
	instr.key  = 'C'
	instr.clef = 'Bass'
	instr.set_range(tuple([Note('E', 1), Note('G', 5)]))
	instr.instrument_nr = instr.names.index('Contrabass')
	return instr

violins.append(Violin())
violins.append(Viola())
violins.append(Cello())
violins.append(Contrabass())

#--------------------------------------------------
# plucked_strings:

def Orchestral_Harp():
	"""Defines and returns an orchestral harp midi instrument (an instance of MidiInstrument())"""

	instr = MidiInstrument()
	instr.name = 'Orchestral Harp'
	instr.key  = 'C'
	instr.clef = 'Treble & Bass'
	instr.set_range(tuple([Note('C', 1), Note('G', 7)]))
	instr.instrument_nr = instr.names.index('Orchestral Harp')
	return instr

plucked_strings.append(Orchestral_Harp())


#--------------------------------------------------
# keyboards:

def Piano():
	"""Defines and returns a piano midi instrument (an instance of MidiInstrument())"""

	instr = MidiInstrument()
	instr.name = 'Piano'
	instr.key  = 'C'
	instr.clef = 'Treble & Bass'
	instr.set_range(tuple([Note('A', 0), Note('C', 8)]))
	instr.instrument_nr = instr.names.index('Acoustic Grand Piano')
	return instr

keyboards.append(Piano())

#--------------------------------------------------
# pitched_percussion:

def Vibraphone():
	"""Defines and returns a vibraphone midi instrument (an instance of MidiInstrument())"""

	instr = MidiInstrument()
	instr.name = 'Vibraphone'
	instr.key  = 'C'
	instr.clef = 'Treble'
	instr.set_range(tuple([Note('F', 3), Note('F', 6)]))
	instr.instrument_nr = instr.names.index('Vibraphone')
	return instr

def Marimba():
	"""Defines and returns a marimba midi instrument (an instance of MidiInstrument())"""

	instr = MidiInstrument()
	instr.name = 'Marimba'
	instr.key  = 'C'
	instr.clef = 'Treble & Bass'
	instr.set_range(tuple([Note('C', 2), Note('C', 7)]))
	instr.instrument_nr = instr.names.index('Marimba')
	return instr

pitched_percussion.append(Vibraphone())
pitched_percussion.append(Marimba())

#--------------------------------------------------
# instruments:

woodwinds 	= {'Clarinets': clarinets, 'Saxophones': saxophones, 'Flutes': flutes}
strings 	= {'Violins': violins, 'Plucked_strings': plucked_strings}
percussion 	= {'Pitched Percussion': pitched_percussion, 'Keyboards': keyboards} 

instruments = {'Woodwinds': woodwinds, 'Strings': strings, 'Percussion': percussion}
