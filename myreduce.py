NOT_PROVIDED = object()

def myreduce(cb, l, initial = NOT_PROVIDED):
	if initial == NOT_PROVIDED:
		if len(l) == 0:
			raise ValueError("empty list with no initial value")
		elif len(l) == 1:
			return l[0]

	accum = initial if initial != NOT_PROVIDED else l[0]
	start = 1 if initial is NOT_PROVIDED else 0
	for i in range(start, len(l)):
		accum = cb(accum, l[i])

	return accum

l = [x for x in range(0, 10, 2)]
print(myreduce(lambda x, y: x+y, l))
print(sum(l))

