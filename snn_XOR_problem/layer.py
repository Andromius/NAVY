from neuron import Neuron
import numpy as np

class Layer:
    def __init__(self, num_neurons, num_inputs, activation_function):
        self.neurons = [Neuron(num_inputs, activation_function) for _ in range(num_neurons)]
        self.outputs = np.zeros(num_neurons)
        self.errors = np.zeros(num_neurons)
        self.deltas = np.zeros(num_neurons)

    def forward(self, inputs):
        self.outputs = [neuron.forward(inputs) for neuron in self.neurons]
        return self.outputs

    def backward(self, errors):
        self.errors = errors
        self.deltas = [neuron.backward(error) for neuron, error in zip(self.neurons, errors)]
        return np.sum(self.deltas, axis=0)
    
    def update_weights(self, learning_rate):
        for neuron in self.neurons:
            neuron.update_weights(learning_rate)

    def print_configuration(self):
        print(f"Layer configuration:")
        print(f"Number of neurons: {len(self.neurons)}")
        for i, neuron in enumerate(self.neurons):
            print(f"Neuron {i+1}: {neuron}")
    