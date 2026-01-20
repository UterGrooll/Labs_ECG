import math

LAB1 = {
    "variant": 5,
    "x1": 1.0,
    "x2": 2.0,
    "points": 200,
    "functions": [
        ("y = e^(-x)", lambda x: math.exp(-x)),
        ("y = 10^(-x)", lambda x: 10 ** (-x)),
    ],
}

LAB2 = {
    "variant": 1,
    "shape": "triangle",
    "x0": 0.0,
    "y0": 0.0,
    "phi": 0,
}

LAB3 = {
    "variant": 4,
    "cube_size": 2.0,
    "alpha_deg": 25.0,
    "beta_deg": 15.0,
    "axis_point": (0.0, 0.0, 0.0),
    "axis_dir": (1.0, 1.0, 0.0),
    "angle_deg": 25.0,
}
