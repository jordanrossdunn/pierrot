import mingus.containers.Instrument as Instrument
import mingus.containers.Note as Note
import string

#--------------------------------------------------

# instrument categories:
woodwinds = {}
strings = {}

# instrument families:

# woodwinds:
clarinets = []
saxophones = []
flutes = []

# strings:
violins = []

# all intruments (by category and family):
instruments = {}

#--------------------------------------------------

def print_instrument_family(family):
	
	print string.ljust('#', 5) + string.ljust('Name', 20) + string.ljust('Key', 10) + string.ljust('Range', 15)
	print '-' * 50
	for index, instr in enumerate(family):
		print string.ljust(str(index+1), 5) + string.ljust(instr.name, 20) + string.ljust(instr.key, 10) + string.ljust(str(instr.range), 15)

def print_instruments():

	for title, category in instruments.iteritems():
		print string.center(" " + title + " ", 50, "~")
		for name, family in category.iteritems():
			print "\n" + string.center(" " + name + " ", 50, "-") + "\n"
			print_instrument_family(family)

#--------------------------------------------------

def get_instrument_families(category):

	families = []
	for name, family in category.iteritems():
		families.append(name)
	return families

def get_instrument_categories():

	categories = []
	for title, category in instruments.iteritems():
		categories.append(title)
	return categories

#--------------------------------------------------
# clarinets:

def Soprano_Clarinet():
	
	instr = Instrument()
	instr.name = 'Soprano Clarinet'
	instr.key  = 'Bb'
	instr.clef = 'Treble'
	instr.set_range(tuple([Note('D', 3), Note('G', 6)]))
	return instr

def Bass_Clarinet():

	instr = Instrument()
	instr.name = 'Bass Clarinet'
	instr.key  = 'Bb'
	instr.clef = 'Treble'
	instr.set_range(tuple([Note('D', 2), Note('G', 5)]))
	return instr

clarinets.append(Soprano_Clarinet())
clarinets.append(Bass_Clarinet())

#--------------------------------------------------
# saxophones:

def Alto_Saxophone():
	
	instr = Instrument()
	instr.name = 'Alto Saxophone'
	instr.key  = 'Eb'
	instr.clef = 'Treble'
	instr.set_range(tuple([Note('Db', 3), Note('A', 5)]))
	return instr

saxophones.append(Alto_Saxophone())

#--------------------------------------------------
# flutes:

def Flute():
	
	instr = Instrument()
	instr.name = 'Flute'
	instr.key  = 'C'
	instr.clef = 'Treble'
	instr.set_range(tuple([Note('C', 3), Note('C', 7)]))
	return instr

flutes.append(Flute())

#--------------------------------------------------
# violins:

def Violin():
	
	instr = Instrument()
	instr.name = 'Violin'
	instr.key  = 'C'
	instr.clef = 'Treble'
	instr.set_range(tuple([Note('G', 3), Note('C', 8)]))
	return instr

violins.append(Violin())

#--------------------------------------------------
# instruments:

woodwinds 	= {'Clarinets': clarinets, 'Saxophones': saxophones, 'Flutes': flutes}
strings 	= {'Violins': violins}

instruments = {'Woodwinds': woodwinds, 'Strings': strings}
