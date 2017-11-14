from utils import mat_to_color, point_to_image_mat
from fractal import Fractal
import matplotlib.pyplot as plt


if __name__ == '__main__':
    mat_points1 = Fractal(point_count=6, selection_limiter=[False, True, False, False, False, False]).execute()
    mat_points2 = Fractal(point_count=6, selection_limiter=[False, False, False, False, False, True]).execute()
    fig, ax = plt.subplots(2)
    h = ax[0].imshow(mat_to_color(point_to_image_mat(mat_points1)))
    h = ax[1].imshow(mat_to_color(point_to_image_mat(mat_points2)))
    plt.show()
