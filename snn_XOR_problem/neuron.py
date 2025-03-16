import numpy as np

class Neuron:
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_derivative(self, x):
        return x * (1 - x)
    
    def tanh(self, x):
        return np.tanh(x)
    
    def tanh_derivative(self, x):
        return 1 - x ** 2
    
    def relu(self, x):
        return np.maximum(0, x)
    
    def relu_derivative(self, x):
        return np.where(x <= 0, 0, 1)
    
    def signum(self, x):
        return np.sign(x)
    
    def signum_derivative(self, x):
        return 1

    def __init__(self, num_inputs, activation_function):
        functions = {
            'sigmoid': [self.sigmoid, self.sigmoid_derivative],
            'tanh': [self.tanh, self.tanh_derivative],
            'relu': [self.relu, self.relu_derivative],
            'signum': [self.signum, self.signum_derivative]
        }

        self.activation_function = functions[activation_function][0]
        self.activation_derivative = functions[activation_function][1]
        self.weights = np.random.uniform(-1, 1, num_inputs)
        self.bias = np.random.uniform(-1, 1)
        self.inputs = 0
        self.output = 0
        self.error = 0
        self.delta_i = 0
        self.net = 0

    def forward(self, inputs):
        self.inputs = inputs
        self.net = np.dot(self.inputs, self.weights) + self.bias
        self.output = self.activation_function(self.net)
        return self.output
    
    def backward(self, error):
        self.error = error
        delta = self.error * self.activation_derivative(self.output)
        self.delta_i = np.dot(self.inputs, delta)
        return np.dot(self.weights, delta)
    
    def update_weights(self, learning_rate):
        self.weights -= learning_rate * self.delta_i
        self.bias -= learning_rate * np.mean(self.delta_i)

    def __str__(self):
        return f"Neuron: {self.weights}, {self.bias}"