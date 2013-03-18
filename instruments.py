import mingus.containers.Instrument as Instrument
import mingus.containers.Note as Note
import string

# instrument categories
woodwinds = {}
strings = {}

# instrument families
# woodwinds
clarinets = []
saxophones = []
flutes = []
# strings
violins = []

# all intruments (by category and family)
instruments = {}

##################################################

def print_instrument_family(family):
	"""Takes an array of extended mingus.containers.Instrument instruments each provided with an 
	additional attribute 'key' and prints their attribute (with the exception of 'clef') values 
	in string formated table."""

	print string.ljust('Name', 25) + string.ljust('Key', 10) + string.ljust('Range', 15)
	print '-' * 50
	for instr in family:
		assert isinstance(family[0], Instrument)
		print string.ljust(instr.name, 25) + string.ljust(instr.key, 10) + string.ljust(str(instr.range), 15)
	#print '-' * 50

def print_instruments():

	for title, category in instruments.iteritems():
		print string.center(" " + title + " ", 50, "~")
		for name, family in category.iteritems():
			print "\n" + string.center(" " + name + " ", 50, "-") + "\n"
			print_instrument_family(family)

def get_instrument_categories():

	categories = []

	for title, category in instruments.iteritems():
		categories.append(title)

	return categories

##################################################
# clarinets

def Soprano_Clarinet():
	"""Returns a mingus.containers.Instrument with attributes assigned for a Bb Soprano Clarinet 
	provided with an additional attribute 'key'."""

	instr = Instrument()
	instr.name = 'Soprano Clarinet'
	instr.key  = 'Bb'
	instr.clef = 'Treble'
	instr.set_range(tuple([Note('D', 3), Note('G', 6)]))
	return instr

def Bass_Clarinet():
	"""Returns a mingus.containers.Instrument with attributes assigned for a Bb Bass Clarinet 
	provided with an additional attribute 'key'."""

	instr = Instrument()
	instr.name = 'Bass Clarinet'
	instr.key  = 'Bb'
	instr.clef = 'Treble'
	instr.set_range(tuple([Note('D', 2), Note('G', 5)]))
	return instr

clarinets.append(Soprano_Clarinet())
clarinets.append(Bass_Clarinet())

##################################################
# saxophones

def Alto_Saxophone():
	"""Returns a mingus.containers.Instrument with attributes assigned for an Eb Alto Saxophone 
	provided with an additional attribute 'key'."""

	instr = Instrument()
	instr.name = 'Alto Saxophone'
	instr.key  = 'Eb'
	instr.clef = 'Treble'
	instr.set_range(tuple([Note('Db', 3), Note('A', 5)]))
	return instr

saxophones.append(Alto_Saxophone())

##################################################
# instruments

woodwinds 	= {'Clarinets': clarinets, 'Saxophones': saxophones, 'Flutes': flutes}
strings 	= {'Violins': violins}

instruments = {'Woodwinds': woodwinds, 'Strings': strings}
