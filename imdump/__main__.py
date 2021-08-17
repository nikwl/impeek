import argparse
import logging
import pathlib

import PIL
from PIL import Image
import numpy as np
from matplotlib import cm

from .fire import fire


def look(input, output, num_imgs, total_width, row_height, vmin, vmax, cmap, rescale):

    if cmap == "fire":
        cmap = fire
    else:
        cmap = cm.get_cmap(cmap)

    logging.info("Searching for files that match: {}".format(input))

    def pad_image(col_stacker):
        # Compute the amount of leftover space on the rhs
        if total_width - cur_w != 0:
            if len(col_stacker[-1].shape) == 2:
                right_pad = np.zeros((row_height, total_width - cur_w))
            elif len(col_stacker[-1].shape) == 3:
                right_pad = np.zeros((row_height, total_width - cur_w, col_stacker[-1].shape[2]))
            else:
                raise RuntimeError()

            # Add the padding
            col_stacker.append(right_pad)

        # Create a single image
        return np.hstack(col_stacker)

    row_stacker = []
    col_stacker = []
    imgs_processed = 0
    cur_w = 0
    for f_in in pathlib.Path(".").glob(input):
        
        # Break early
        if imgs_processed >= num_imgs:
            break        

        # Try to load the next image
        logging.debug("Attempting to load file {}".format(f_in))
        try:
            img =  Image.open(f_in)
        except PIL.UnidentifiedImageError:
            continue
        logging.debug("Loaded image with shape {} from {}".format(img.size, f_in))
        
        # Resize image to correct dimension
        img_w, img_h = img.size
        new_w = int((row_height / img_h) * img_w)
        img = img.resize((new_w, row_height))
        img_w, img_h = img.size

        # If the image is really big, resize it so that it takes up a whole column
        if img_w >= total_width:
            new_h = int((total_width / img_w) * img_h)
            img = img.resize((total_width, new_h))
            img_w, img_h = img.size
        logging.debug("Resized image to {}".format(img.size))

        # If the next image would overflow the current column, start a new column
        if cur_w + img_w > total_width:
            # Create a single image from the current column, add to the stack
            row_stacker.append(pad_image(col_stacker))

            # Reset the current column
            col_stacker = []
            cur_w = 0

        # Convert to numpy array
        img = np.array(img)

        # Make the image optimally viewable
        if rescale:
            if vmin is None:
                _min = img.min()
            else:
                _min = vmin
            if vmax is None:
                _max = img.max()
            else:
                _max = vmin
            img = np.clip((img - _min) / (_max - _min), 0.0, 1.0) * 255

        # Can we apply a colormap?
        if cmap is not None and \
            (len(img.shape) == 2 or (len(img.shape) == 3 and img.shape[-1] == 1)
        ):  
            img = (cmap(img / 255) * 255)

        # Convert back to a PIL image
        img = Image.fromarray(img.astype(np.uint8))

        # Add to the current column
        cur_w += img_w
        imgs_processed += 1
        col_stacker.append(np.array(img.convert("RGB")))

    if len(col_stacker) == 0:
        logging.info("No images found")
        return

    # Create a single image from the current column, add to the stack
    row_stacker.append(pad_image(col_stacker))

    # Save
    logging.info("Saving image to {}".format(output))
    Image.fromarray(np.vstack(row_stacker).astype(np.uint8)).save(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A script to create a single collage of images from many"
        + "images saved on disk. Can handle any image type. Can be called "
        + "recursively. Can be passed a regular expression to be matched to  "
        + "specific types of images, or specific naming patterns."
    )
    parser.add_argument(
        dest="input", 
        type=str, 
        help="Path to the directory containing the image files."
    )
    parser.add_argument(
        dest="output", 
        type=str, 
        help="Path that the output image will be saved to."
    )
    parser.add_argument(
        "--num_imgs",
        type=int,
        default=100,
        help="How many images in total (maximum) should be displayed."
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1920,
        help="Output image width, in pixels."
    )
    parser.add_argument(
        "--row_height",
        type=int,
        default=480,
        help="Hight of each row of images, in pixels."
    )
    parser.add_argument(
        "--vmin", 
        type=int, 
        default=None,
        help="",
    )
    parser.add_argument(
        "--vmax",
        type=int,
        default=None,
        help="",
    )    
    parser.add_argument(
        "--cmap",
        default="jet",
        type=str, 
        help="Colormap to use."
    )
    parser.add_argument(
        "--rescale",
        action="store_true",
        default=False,
        help="If passed will rescale the image values such that they are optimally " 
        + "visible. Use vmin and vmax to define a specific rescale range."
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
        args.output, 
        args.num_imgs, 
        args.width,
        args.row_height, 
        args.vmin,
        args.vmax,
        args.cmap,
        args.rescale,
    )