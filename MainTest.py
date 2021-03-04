import LibraryNeuralNetwork as lnn

nn = lnn.NeuralNetwork(size=[2, 1])
print(str(nn))
print(repr(nn))
nn.evaluate([1, 5])
print(str(nn))
print(repr(nn))