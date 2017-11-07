from utils import mat_to_color, point_to_image_mat
import random
import matplotlib.pyplot as plt
import math
import numba as nb
import numpy as np


@nb.jit(nopython=True)
def instantiate_points(point_count):
    # Creates points on a unit circle of count pointCount
    # The radius of this circle is 1
    points = np.zeros((point_count, 2))
    for i in range(point_count):
        const = 2 * math.pi * i / point_count
        x, y = math.sin(const), math.cos(const)
        points[i] = [x, y]

    return points


@nb.jit(nopython=True)
def choices(conditionArray):
    pointCount = len(conditionArray)
    choice = random.randint(0, pointCount - 1)

    while True:
        for _ in range(100):
            # Loop until we find an index that has a true value in conditionArray
            potential_choice = random.randint(0, pointCount - 1)
            idx = int((potential_choice - choice) % pointCount)
            if not conditionArray[idx]:
                choice = potential_choice
                yield choice


@nb.jit(nb.types.UniTuple(nb.float64, 2)(nb.float64, nb.float64, nb.float64, nb.float64, nb.int16), nopython=True)
def create_point(pointx, pointy, edgex, edgey, scaling_factor=2):
    return ((pointx + edgex) / scaling_factor, (pointy + edgey) / scaling_factor)


@nb.jit(nopython=True)
def fractal_loop(selection_limiter, scaling_factor, iters, dry_fire, point_count):
    gen_choice = choices(selection_limiter)
    point = (random.uniform(-1, 1), random.uniform(-1, 1))
    points_array = instantiate_points(point_count)
    mat = np.zeros((iters, 2))
    for i in range(-dry_fire, iters):
        choice = points_array[next(gen_choice)]
        point = create_point(point[0], point[1], choice[0], choice[1],
                             scaling_factor=scaling_factor)
        if i >= 0:
            mat[i] = point
    return mat


def fractal(iters=50000, dry_fire=1000, point_count=3,
            scaling_factor=2, selection_limiter=None):
    if selection_limiter is None:
        selection_limiter = [False] * point_count

    return fractal_loop(selection_limiter, scaling_factor, iters, dry_fire, point_count)


if __name__ == '__main__':
    mat = fractal()
    fig, ax = plt.subplots()
    h = ax.imshow(mat_to_color(point_to_image_mat(mat)))
    plt.show()
