import numpy as np
import struct


def hex_to_rgb(hexstr):
    return struct.unpack('BBB', b''.fromhex(hexstr))


def mat_to_color(mat, colors=((66, 66, 111), (244, 164, 96))):
    colors = np.array(colors)
    index = np.digitize(mat.ravel(), [0, 1], right=True)
    return colors[index].reshape(mat.shape + (3,)).astype(np.uint8)


def point_to_image_mat(mat, img_size=(500, 500)):
    mat = np.array(mat).T
    x_max, x_min = mat[0].max(), mat[0].min()
    y_max, y_min = mat[1].max(), mat[1].min()
    x_rng, y_rng = x_max - x_min, y_max - y_min
    mul_factor_x = (img_size[0] - 1) / x_rng
    mul_factor_y = (img_size[1] - 1) / y_rng
    img = np.zeros(img_size)
    for x, y in mat.T:
        # TODO: Increment by 1 instead of set to 1 to keep track of the number of times a pixel appears
        img[int((x - x_min) * mul_factor_x), int((y - y_min) * mul_factor_y)] = 1
    return img
