import numpy as np

MODELS = [
    [
        (  # First transformation
            np.array([
                [0.00, 0.00, 0.01],
                [0.00, 0.26, 0.00],
                [0.00, 0.00, 0.05]
            ]),
            np.array([0.00, 0.00, 0.00])
        ),
        (  # Second transformation
            np.array([
                [0.20, -0.26, -0.01],
                [0.23,  0.22, -0.07],
                [0.07,  0.00,  0.24]
            ]),
            np.array([0.00, 0.80, 0.00])
        ),
        (  # Third transformation
            np.array([
                [-0.25, 0.28,  0.01],
                [ 0.26, 0.24, -0.07],
                [ 0.07, 0.00,  0.24]
            ]),
            np.array([0.00, 0.22, 0.00])
        ),
        (  # Fourth transformation
            np.array([
                [ 0.85,  0.04, -0.01],
                [-0.04,  0.85,  0.09],
                [ 0.00,  0.08,  0.84]
            ]),
            np.array([0.00, 0.80, 0.00])
        )
    ],
    [
        (  # First transformation
            np.array([
                [0.05, 0.00, 0.00],
                [0.00, 0.60, 0.00],
                [0.00, 0.00, 0.05]
            ]),
            np.array([0.00, 0.00, 0.00])
        ),
        (  # Second transformation
            np.array([
                [ 0.45, -0.22,  0.22],
                [ 0.22,  0.45,  0.22],
                [ -0.22, -0.22,  0.45]
            ]),
            np.array([0.00, 1.00, 0.00])
        ),
        (  # Third transformation
            np.array([
                [-0.45,  0.22, -0.22],
                [ 0.22,  0.45,  0.22],
                [0.22,  -0.22,  0.45]
            ]),
            np.array([0.00, 1.25, 0.00])
        ),
        (  # Fourth transformation
            np.array([
                [ 0.49, -0.08,  0.08],
                [ 0.08,  0.49,  0.08],
                [ 0.08, -0.08,  0.49]
            ]),
            np.array([0.00, 2.00, 0.00])
        )
    ]
]