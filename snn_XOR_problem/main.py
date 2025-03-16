from neural_network import NeuralNetwork
from layer import Layer
import numpy as np
import matplotlib.pyplot as plt

def plot_error_history(error_history):
    plt.figure()
    plt.plot(error_history)
    plt.xlabel('Epochs')
    plt.ylabel('Error')
    plt.title('Error History')

def plot_decision_boundary(nn: NeuralNetwork, inputs, targets):
    x_min, x_max = -0.5, 1.5
    y_min, y_max = -0.5, 1.5
    h = 0.01
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = np.array([nn.predict([x, y]) for x, y in zip(xx.ravel(), yy.ravel())])
    Z = Z.reshape(xx.shape)
    
    plt.figure()
    plt.contourf(xx, yy, Z, alpha=0.8)
    plt.scatter([x[0] for x in inputs], [x[1] for x in inputs], c=[y[0] for y in targets], edgecolors='k', marker='o')
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.xlabel('Input 1')
    plt.ylabel('Input 2')
    plt.title('Decision Boundary for XOR Problem')

def main():
    inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
    targets = [[0], [1], [1], [0]]

    np.random.seed(46)
    layers = [
        Layer(2, 2, 'sigmoid'),
        Layer(1, 2, 'sigmoid')
    ]
    nn = NeuralNetwork(layers, learning_rate=0.1, epochs=10_000, debug=True)
    nn.print_configuration()
    nn.fit(inputs, targets)
    nn.print_configuration()
    
    print(f"Error: {nn.final_error}")
    for i in range(len(inputs)):
        print(f"Input: {inputs[i]}, True: {targets[i]}, Prediction: {nn.predict(inputs[i])}")
        
    plot_decision_boundary(nn, inputs, targets)
    plot_error_history(nn.error_history)
    plt.show()

if __name__ == '__main__':
    main()