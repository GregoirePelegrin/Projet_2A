def activ_func(a, b):
	if a and b:			# AND
		return True
	return False
	# if a or b:		# OR
	# 	return True
	# return False

class Perceptron:
	def __init__(self, _state=False):
		self.inputList = []
		self.state = _state

	def add_input(self, pIn):
		self.inputList.append(pIn)

	def evaluate(self):
		if len(self.inputList) != 2:
			print("Error in network build")
			return False
		self.state = activ_func(self.inputList[0].state, self.inputList[1].state)
		return self.state

p11 = Perceptron(True)
p12 = Perceptron()
p21 = Perceptron()
p22 = Perceptron()
p3 = Perceptron()
p21.add_input(p11)
p21.add_input(p12)
p22.add_input(p11)
p22.add_input(p12)
p3.add_input(p21)
p3.add_input(p22)

p21.evaluate()
p22.evaluate()
p3.evaluate()

print(p3.state)