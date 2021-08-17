import argparse
import logging
import pathlib
import io
from argparse import RawTextHelpFormatter

import PIL
from PIL import Image
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt

import cv2

from .fire import fire

ARROW_KEYS = {
    'up': [82, 119],
    'down': [84, 115],
    'left': [81, 97],
    'right': [83, 100]
}

def plt2np():
    with io.BytesIO() as buff:
        plt.savefig(buff, format='raw')
        buff.seek(0)
        data = np.frombuffer(buff.getvalue(), dtype=np.uint8)
    w, h = plt.gca().figure.canvas.get_width_height()
    return data.reshape((int(h), int(w), -1))

def look(input, vmin, vmax, cmap, rescale, use_mpl, scale):

    if cmap == "fire":
        cmap = fire
    else:
        cmap = cm.get_cmap(cmap)

    logging.info("Searching for files that match: {}".format(input))

    img_queue = []
    ptr = -1
    iterator = pathlib.Path(".").glob(input)

    while True:
        if ptr >= len(img_queue) or len(img_queue) == 0:
            try:
                # Load the next image
                while True:
                    f_in = next(iterator)
                    try:
                        img = np.array(Image.open(f_in))
                        break
                    except PIL.UnidentifiedImageError:
                        pass
                    
                if use_mpl:
                    plt.imshow(np.array(img), cmap=cmap, vmin=vmin, vmax=vmax)
                    plt.colorbar()
                    img = plt2np()
                    plt.close()
                else:
                    # Make the image optimally viewable
                    if rescale:
                        if vmin is None:
                            _min = img.min()
                        else:
                            _min = vmin
                        if vmax is None:
                            _max = img.max()
                        else:
                            _max = vmax
                        img = np.clip((img - _min) / (_max - _min), 0.0, 1.0) * 255

                    # Can we apply a colormap?
                    if cmap is not None and \
                        (len(img.shape) == 2 or (len(img.shape) == 3 and img.shape[-1] == 1)
                    ):  
                        img = (cmap(img / 255) * 255)
                    
                # Standardize the image size
                img = Image.fromarray(img.astype(np.uint8)).convert("RGB")
                img = img.resize((np.array(img.size)*scale).astype(int), Image.ANTIALIAS)
                img = np.array(np.array(img))

                # Append to the queue
                img_queue.append((str(f_in), img))
            except StopIteration:
                ptr = len(img_queue)-1
                logging.debug("Reached end of list")
        elif ptr <= 0:
            logging.debug("Reached beginning of list")
            ptr = 0

        if len(img_queue) == 0:
            logging.info("No images found")
            break
        
        logging.info("Displaying image: {}".format(img_queue[ptr][0]))

        # Show the image
        cv2.imshow(input, cv2.cvtColor(img_queue[ptr][1], cv2.COLOR_BGR2RGB))

        # Get input from the user
        keypress = cv2.waitKey(0)
        if keypress in ARROW_KEYS['right']:
            ptr += 1
        elif keypress in ARROW_KEYS['left']:
            ptr -= 1
        elif keypress == ord('q'):
            break
        logging.debug("Got keypress: {}".format(keypress))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script to quickly 'peek' at images on disk. Call with a "
        + "regular expression to traverse multiple directories or traverse "
        + "directories recursively. Call with '--rescale' to automatically "
        + "rescale the pixel values such that they fall between 0 and 255. "
        + "Call with a '--cmap' to apply a colormap to single-channel images. "
        + "Call with '--use_mpl' to use the matplotlib backend which will "
        + "display raw color values with a colorbar. Must be called as a module. \n\n"
        + "example: python -m impeek \"../**/*.png\" --cmap fire\n"
        + "  Display all png images in any directory rooted above the current "
        + "directory, using fire colormap.",
        formatter_class=RawTextHelpFormatter
    )
    parser.add_argument(
        dest="input", 
        type=str, 
        help="A regular expression used to find files. If you use the '*' operator "
        + "you will need to enclose this argument in double quotes."
    )
    parser.add_argument(
        "--vmin", 
        type=int, 
        default=None,
        help="Minimum pixel intensity value to display. All pixel values lower "
        + "than this will be clipped to 0."
    )
    parser.add_argument(
        "--vmax",
        type=int,
        default=None,
        help="Maximum pixel intensity value to display. All pixel values higher "
        + "than this will be clipped to 255."
    )    
    parser.add_argument(
        "--cmap",
        default="fire",
        type=str, 
        help="Colormap to use. Single channel images will be converted to RGB "
        + "using this colormap. Has no effect on multi-channel (color) images."
    )
    parser.add_argument(
        "--rescale",
        action="store_true",
        default=False,
        help="If passed will rescale the pixel values such that they fall between "
        + "0 and 255. By default uses the min and max values of the image to " 
        + "scale the pixel values. If vmin or vmax are passed these are used "
        + "instead."
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=1.0,
        help="Apply a dimensional scale to the image. Default is 1.0."
    )
    parser.add_argument(
        "--use_mpl",
        action="store_true",
        default=False,
        help="If true will use the matplotlib engine to display the image. See "
        + "the documentation for matplotlib.imshow for more information. This "
        + "will also display a colorbar with the raw pixel values before rescaling."
    )
    parser.add_argument(
        "--debug",
        default=False,
        action="store_true",
        help="If set, debugging messages will be printed.",
    )
    parser.add_argument(
        "--quiet",
        default=False,
        action="store_true",
        help="If set, only warnings will be printed.",
    )
    args = parser.parse_args()

    # Configure logging
    logger = logging.getLogger()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    elif args.quiet:
        logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.INFO)
    logger_handler = logging.StreamHandler()
    logger.addHandler(logger_handler)

    look(
        args.input, 
        args.vmin,
        args.vmax,
        args.cmap,
        args.rescale,
        args.use_mpl,
        args.scale,
    )