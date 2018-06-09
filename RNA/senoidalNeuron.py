import numpy as np

def sigmoid(sum):
    return 1 / (1 + np.exp(-sum))

def sigmoidDerivate(sig):
    return sig * (1 - sig)

inputs = np.array([[0,0],
                     [0,1],
                     [1,0],
                     [1,1]])

output = np.array([[0],[1],[1],[0]])

weights0 = 2*np.random.random((2,3)) - 1
weights1 = 2*np.random.random((3,1)) - 1

# time of train
epoch = 1000000
learningRate = 0.5
moment = 1

for j in range(epoch):
    inputLayer = inputs
    sumSinapse0 = np.dot(inputLayer, weights0)
    hiddenLayer = sigmoid(sumSinapse0)

    sumSinapse1 = np.dot(hiddenLayer, weights1)
    outputLayer = sigmoid(sumSinapse1)

    errorOutputLayer = output - outputLayer
    absoluteMean = np.mean(np.abs(errorOutputLayer))
    print("Error: " + str(absoluteMean))

    outputDerivate = sigmoidDerivate(outputLayer)
    outputDelta = errorOutputLayer * outputDerivate

    weights1Transposed = weights1.T
    outputDeltaXWeight = outputDelta.dot(weights1Transposed)
    deltahiddenLayer = outputDeltaXWeight * sigmoidDerivate(hiddenLayer)

    hiddenLayerTransposed = hiddenLayer.T
    newWeights1 = hiddenLayerTransposed.dot(outputDelta)
    weights1 = (weights1 * moment) + (newWeights1 * learningRate)

    inputLayerTransposed = inputLayer.T
    newWeights0 = inputLayerTransposed.dot(deltahiddenLayer)
    weights0 = (weights0 * moment) + (newWeights0 * learningRate)

print outputLayer
