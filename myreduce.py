NOT_PROVIDED = object()

def myreduce(cb, l, initial = NOT_PROVIDED):
	i = iter(l)

	if initial is NOT_PROVIDED:
		try:
			accum = next(i)
		except StopIteration:
			raise ValueError("empty list with no initial value")
	else:
		accum = initial

	for x in i:
		accum = cb(accum, x)

	return accum