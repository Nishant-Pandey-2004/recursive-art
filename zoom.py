from PIL import Image
from numpy import average, array, sqrt  # Import sqrt function from numpy

# modify these params#
INNER_SIZE = 360
INNER_X_LEFT = 2665
INNER_Y_TOP = 1290
STEPS = 50
GIF_RES = 1000
DURATION = 20
MODE = "linear"  # or quad or sqrt
IMAGE = "zoom.png"

# init helper data structures
image = Image.open(IMAGE)
crop_start = array([0, 0, image.size[0], image.size[1]])
crop_end = array([INNER_X_LEFT, INNER_Y_TOP, INNER_X_LEFT + INNER_SIZE, INNER_Y_TOP + INNER_SIZE])
frames = []


def zoom_image(start, end, step):
    if step <= STEPS:
        mode = {"linear": [STEPS - step, step], "quad": [(STEPS - step) ** 2, step ** 2], "sqrt": [sqrt(STEPS - step), sqrt(step)]}
        new_dim = average([start, end], weights=mode[MODE], axis=0)
        frames.append(image.crop(new_dim).resize((GIF_RES, GIF_RES)))
        zoom_image(start, end, step + 1)


zoom_image(crop_start, crop_end, 0)

# save output
frames[0].save(MODE + '.gif', format='GIF', append_images=frames[1:], save_all=True, duration=DURATION, loop=0)
