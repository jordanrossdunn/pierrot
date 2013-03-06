import mingus.core.value as value

def get_relative_durations():
	
	relative_durations = 	{'base-value': [], 'tuplet-3': [], 'tuplet-5': [], 'tuplet-7': [],
							'dotted-1': [], 'dotted-2': [], 'dotted-3': []}

	relative_durations['base-value'].extend(value.base_values)
	relative_durations['tuplet-3'].extend(value.base_triplets)
	relative_durations['tuplet-5'].extend(value.base_quintuplets)
	relative_durations['tuplet-7'].extend(value.base_septuplets)

	for item in value.base_values:
		relative_durations['dotted-1'].append(value.dots(item))
		relative_durations['dotted-2'].append(value.dots(item, 2))
		relative_durations['dotted-3'].append(value.dots(item, 3))

	return relative_durations

def is_in_relative_durations(val):

	for key, item in get_relative_durations().iteritems():
		for element in item:
			if val == element:
				return True
	return False

