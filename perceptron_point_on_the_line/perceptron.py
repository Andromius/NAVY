import numpy as np

class Perceptron:
    def _signum(self, input):
        result = np.multiply(input, self._weights)
        return np.sign(np.sum(result) + self._bias)

    def _calculate_error(self, true, guess):
        return true - guess
    
    def _adjust_weights(self, error, input):
        for i, weight in enumerate(self._weights):
            self._weights[i] = weight + error * input[i] * self._learning_rate

    def _adjust_bias(self, error):
        self._bias = self._bias + error * self._learning_rate
    
    def __str__(self):
        string = 'Perceptron configuration:\n\n'
        string += f'Learning rate: {self._learning_rate}\nBias: {self._bias}\nWeights: {self._weights}\nActivation function: {self._activation_function.__name__}\n'
        return string

    def __init__(self, max_iterations = 10000, weights = np.array([0.2, 0.4]), bias = 0.5, learning_rate = 0.1):
        self._max_iterations = max_iterations
        self._learning_rate = learning_rate
        self._bias = bias
        self._activation_function = self._signum
        self._weights = weights if weights is not None else np.random.uniform(-1, 1, 2)

    def train(self, input, true_labels):
        input_length = len(input)
        for iteration in range(self._max_iterations):
            for i in range(input_length):
                guess = self._activation_function(input[i])
                error = self._calculate_error(true_labels[i], guess)
                
                self._adjust_weights(error, input[i])
                self._adjust_bias(error)
    
    def predict(self, input):
        predictions = []
        for value in input:
            prediction = self._activation_function(value)
            predictions.append(prediction)
        return np.array(predictions)

    def get_weights(self):
        return np.copy(self._weights)
    
    def get_bias(self):
        return self._bias

