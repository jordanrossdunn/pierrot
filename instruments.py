import mingus.containers.Instrument as Instrument
import mingus.containers.Note as Note
import string

def print_family(family):
	"""Takes an array of extended mingus.containers.Instrument instruments each provided with an 
	additional attribute 'key' and prints their attribute (with the exception of 'clef') values 
	in string formated table."""

	print "\n"
	print string.ljust('Name', 25) + string.ljust('Key', 10) + string.ljust('Range', 15)
	print '-' * 50
	for instr in family:
		assert isinstance(family[0], Instrument)
		print string.ljust(instr.name, 25) + string.ljust(instr.key, 10) + string.ljust(str(instr.range), 15)
	print "\n"

def Soprano_Clarinet():
	"""Returns a mingus.containers.Instrument with attributes assigned for a Bb Soprano Clarinet 
	provided with an additional attribute 'key'."""

	instr = Instrument()
	instr.name = 'soprano clarinet'
	instr.key  = 'Bb'
	instr.clef = 'treble'
	instr.set_range(tuple([Note('D', 3), Note('G', 6)]))
	return instr

def Bass_Clarinet():
	"""Returns a mingus.containers.Instrument with attributes assigned for a Bb Bass Clarinet 
	provided with an additional attribute 'key'."""

	instr = Instrument()
	instr.name = 'bass clarinet'
	instr.key  = 'Bb'
	instr.clef = 'treble'
	instr.set_range(tuple([Note('D', 2), Note('G', 5)]))
	return instr

clarinets = []
clarinets.append(Soprano_Clarinet())
clarinets.append(Bass_Clarinet())

def Alto_Saxophone():
	"""Returns a mingus.containers.Instrument with attributes assigned for an Eb Alto Saxophone 
	provided with an additional attribute 'key'."""

	instr = Instrument()
	instr.name = 'alto saxophone'
	instr.key  = 'Eb'
	instr.clef = 'treble'
	instr.set_range(tuple([Note('Db', 3), Note('A', 5)]))
	return instr
