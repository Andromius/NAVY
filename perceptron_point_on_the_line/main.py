from perceptron import Perceptron
import numpy as np
import matplotlib.pyplot as plt

def linear_func_factory(a, b):
    def f(x):
        return a * x + b
    return f

def perceptron_line(weights, bias, x):
    f = linear_func_factory(weights[0], bias)
    return -f(x) / weights[1]

def generate_points(count, low=-3, high=3):
    return np.random.uniform(low, high, (count, 2))

def get_true_labels(points, function):
    labels = []
    for point in points:
        y = function(point[0])
        labels.append(0 if y == point[1] else (-1 if y > point[1] else 1))
    return labels

def visualize_perceptron(points, predictions, target_function, perceptron: Perceptron, low=-3, high=3):
    plt.scatter(points[:, 0], points[:, 1], c=predictions, cmap='coolwarm', alpha=0.5)
    
    x_values = np.linspace(low, high, 100)
    y_values = target_function(x_values)
    plt.plot(x_values, y_values, color='black', label='Cílová funkce', linewidth=1)

    plt.axhline(0, color='grey', linewidth=0.5)
    plt.axvline(0, color='grey', linewidth=0.5)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Perceptron Predictions and Target Function')

    y_perceptron = perceptron_line(perceptron.get_weights(), perceptron.get_bias(), points[:, 0])
    plt.plot(points[:, 0], y_perceptron, color='green', label='Rozhodovací hranice', linewidth=0.5)
    plt.legend()
    
    offset_low = low - 1
    offset_high = high + 1 
    plt.xlim(offset_low, offset_high)
    plt.ylim(offset_low, offset_high)
    
    plt.show()

if __name__ == '__main__':    
    points = generate_points(100)
    target_function = linear_func_factory(3, 2)
    true_labels = get_true_labels(points, target_function)

    perceptron = Perceptron()
    print(perceptron)
    perceptron.train(points, true_labels)
    print(perceptron)

    predictions = perceptron.predict(points)
    visualize_perceptron(points, predictions, target_function, perceptron)


