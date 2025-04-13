from random import choice
import numpy as np
import preset_models
import matplotlib.pyplot as plt

def visualize_points(points):
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    points = np.array(points)
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], c='b')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

def apply_transform(point: np.ndarray, transform: np.ndarray, translate: np.ndarray) -> np.ndarray:
    point = transform @ point + translate
    return point

def ifs(point, iterations, transforms):
    points = []
    points.append(np.copy(point))
    for iteration in range(iterations):
        transform = choice(transforms)
        point = apply_transform(point, transform[0], transform[1])
        points.append(np.copy(point))
    return points

def main():
    start_point = np.zeros(3)
    iterations = 1500
    
    visualize_points(ifs(start_point, iterations, preset_models.MODELS[0]))
    visualize_points(ifs(start_point, iterations, preset_models.MODELS[1]))

    plt.show()

if __name__ == "__main__":
    main()
