import numpy as np
from layer import Layer

class NeuralNetwork:
    def __init__(self, layers: list[Layer], learning_rate=0.1, epochs=10000, debug=False):
        self.layers = layers
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.total_error = 0
        self.debug = debug

    def forward(self, inputs):
        for layer in self.layers:
            inputs = layer.forward(inputs)
        return inputs

    def backward(self, target):
        errors = -np.subtract(target, self.layers[-1].outputs)
        for layer in reversed(self.layers):
            errors = layer.backward(errors)
            layer.update_weights(self.learning_rate)
        return errors

    def calculate_error(self, targets):
        return np.sum(np.square(np.subtract(targets, self.layers[-1].outputs)) * 0.5)
    
    def fit(self, inputs, targets):
        for _ in range(self.epochs):
            self.total_error = 0
            for i in range(len(inputs)):
                self.forward(inputs[i].copy())
                self.backward(targets[i].copy())
                self.total_error += self.calculate_error(targets[i])
            if self.debug and _ % 1000 == 0:
                print(f"Epoch: {_}")
                print(f"Total error: {self.total_error}")
                print()

    def predict(self, inputs):
        return np.round(self.forward(inputs))
    
    def print_configuration(self):
        print(f"Neural network configuration:")
        print(f"Number of layers: {len(self.layers)}")
        for i, layer in enumerate(self.layers):
            layer.print_configuration()
            print()
