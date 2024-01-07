"""
Module: examples

Some example code using images.

Authors:
1) Sat Garcia (sat@sandiego.edu)
"""

import comp110_image


def double(img):
    """
    Returns a new image that is the same as the original, but twice as wide
    and twice as high.

    Params:
    img (type: Picture) - The original picture.

    Returns:
    (type: Picture) - A new picture that is the same as the original (img),
        but with twice the height and twice the width.
    """

    bigger_img = comp110_image.Picture(img.getWidth()*2, img.getHeight()*2)
    for x in range(bigger_img.getWidth()):
        for y in range(bigger_img.getHeight()):
            orig_x = x // 2
            orig_y = y // 2
            orig_pixel = img.getPixel(orig_x, orig_y)
            bigger_img.setPixel(x, y, orig_pixel)

    return bigger_img


def negative(img):
    """ Applies the 'negative' filter to img. """
    for row in range(img.getHeight()):
        for col in range(img.getWidth()):
            pix = img.getPixel(col, row)
            pix.setRed(255 - pix.getRed())
            pix.setGreen(255 - pix.getGreen())
            pix.setBlue(255 - pix.getBlue())

