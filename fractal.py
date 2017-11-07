import math
import numba as nb
import numpy as np
import random
from ValidatingObject import ValidatingObject


@nb.jit(nopython=True)
def instantiate_points(point_count):
    """
    Creates points on a unit circle of count pointCount
    The radius of this circle is 1
    :int point_count: Number of points on unit circle
    """
    points = np.zeros((point_count, 2))
    for i in range(point_count):
        const = 2 * math.pi * i / point_count
        x, y = math.sin(const), math.cos(const)
        points[i] = [x, y]

    return points


@nb.jit(nopython=True)
def choices(selection_limiter):
    """
    Generator that provides choices for the flam3 algorithm.
    Selection limiter is an array of booleans that limits choices.

    If selection_limiter[0] = True then the same choice
    can never be selected twice in a row.

    If selection_limiter[1] = True then the new choice has to be at least
    2 points away.

    TODO: Cache choices.
    TODO: Change selection_limiter to array of int such that the following numbers
    denote an action dependent on the cache of choices:
        - selection_limiter[0] = 0
          The choice cannot be repeated twice in a row
        - selection_limiter[0] = 1
          The choice cannot be repeated every other run
        - selection_limiter[1] = [1,2]
          selection_limiter[3] = [1,2]
          The choice cannot be repeated 1 or 3  places from the
          two previously chosen choices


    :boolean[:] selection_limiter: Limiter array
    """
    point_count = len(selection_limiter)
    choice = random.randint(0, point_count - 1)
    cached_choices = [choice]
    loop_counter = 0
    while True:
        # Loop until we find an index that has a true value in conditionArray

        # Make sure we don't encounter an infinite loop
        loop_counter += 1
        if loop_counter > 200:
            raise Exception('Choices generator encountered an infinite loop.')

        # Try for a new choice using the selection_limiter
        potential_choice = random.randint(0, point_count - 1)
        idx = int((potential_choice - choice) % point_count)
        if not selection_limiter[idx]:
            choice = potential_choice
            cached_choices.append(choice)
            loop_counter = 0
            yield choice


@nb.jit(nb.types.UniTuple(nb.float64, 2)(nb.float64, nb.float64, nb.float64, nb.float64, nb.int16), nopython=True)
def create_point(point_x, point_y, edge_x, edge_y, scaling_factor=2):
    return (point_x + edge_x) / scaling_factor, (point_y + edge_y) / scaling_factor


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


class Fractal(ValidatingObject):
    """
    A ValidatingObject with a set of default PARAMS to create a nice-looking
    Sierpinski triangle.
    """
    PARAMS = {'run_count': 50000, 'dry_fire': 1000, 'point_count': 3,
              'scaling_factor': 2, 'selection_limiter': None}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__dict__.update(self.__class__.PARAMS)
        self.validate()

    def validate(self):
        if self.point_count <= 0:
            raise Exception('Point count cannot be 0!')

        if self.selection_limiter is None:
            self.selection_limiter = [False] * self.point_count

        if len(self.selection_limiter) != self.point_count:
            raise Exception('Selection limiter is not equal to point count!')

    def execute(self):
        self.validate()
        return fractal_loop(self.selection_limiter, self.scaling_factor, self.run_count,
                            self.dry_fire, self.point_count)
