from utils import mat_to_color, point_to_image_mat
from fractal import Fractal
import matplotlib.pyplot as plt


if __name__ == '__main__':
    mat_points = Fractal(point_count=5, selection_limiter=[False, False, False, False, False]).execute()
    fig, ax = plt.subplots()
    h = ax.imshow(mat_to_color(point_to_image_mat(mat_points)))
    plt.show()
