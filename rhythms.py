import mingus.core.value as value

def get_valid_durations():
	
	valid_durations = 	{'base': [], 'triplet': [], 'quintuplet': [], 'septuplet': [],
						'single-dotted': [], 'double-dotted': [], 'triple-dotted': []}

	valid_durations['base'].extend(value.base_values)
	valid_durations['triplet'].extend(value.base_triplets)
	valid_durations['quintuplet'].extend(value.base_quintuplets)
	valid_durations['septuplet'].extend(value.base_septuplets)

	for item in value.base_values:
		valid_durations['single-dotted'].append(value.dots(item))
		valid_durations['double-dotted'].append(value.dots(item, 2))
		valid_durations['triple-dotted'].append(value.dots(item, 3))

	return valid_durations

def is_valid_duration(duration):

	for key, item in get_valid_durations().iteritems():
		for value in item:
			if duration == value:
				return True
	return False

