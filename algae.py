def next_gen(gen):
	output = ''
	for char in gen:
		if char == 'A':
			output += 'AB'
		elif char == 'B':
			output += 'A'
	return output

def print_gen(gen):
	print gen.replace('A', '*').replace('B', '.')

gen = 'A'

for i in xrange(10):
	print_gen(gen)
	gen = next_gen(gen)
