"""
Module: collage_creator

A program to create an Andy Warhol-style collage.

Authors:
1) Will Dobrzanski - USD Email Address
2) Antonio Barcelos - USD Email Address
"""

import comp110_image
import math

def copy_to(src_img, dest_img, start_x, start_y):
    """
    Copies one image into another, start at the given starting coordinate.

    DO NOT MODIFY THIS FUNCTION!!!

    Parameters:
    src_img (type: Picture) - The picture to copy.
    dest_img (type: Picture) - The picture to copy into.
    start_x (type: int) - The column where we start copying to dest_img.
    start_y (type: int) - The row where we start copying to dest_img.
    """
    for x in range(src_img.getWidth()):
        for y in range(src_img.getHeight()):
            srcPixel = src_img.getPixel(x,y)
            dest_img.setPixel(x + start_x, y + start_y, srcPixel)

def unique_filter(img):

    """
    Creates filter that makes the image brighter

    Parameters:
    img(type: Image)

    Returns
    pic0(Type: image)

    """
    
    pic0 = img.copy()
    x = img.getHeight()
    for row in range(x):
        for col in range(img.getWidth()):
            p = pic0.getPixel(col, row)

            red = p.getRed()
            green = p.getGreen()
            blue = p.getBlue()


            red = red * 1.5
            green = green * 1.5
            blue = blue * 1.5

            if red < 0:
                red = 0
            elif red > 255:
                red = 255
            
            if green < 0:
                green = 0
            elif green > 255:
                green = 255

            if blue < 0:
                blue = 0
            elif blue > 255:
                blue = 255

            p.setRed(int(red))
            p.setGreen(int(green))
            p.setBlue(int(blue))

    
    return pic0

def apply_kernel(img, filtered_img, x, y, kernel):
    """
    Applies the given kernel to the pixel in img at (x,y).

    Params:
    img (type: Picture) - The original (unmodified) image.
    filtered_img (type: Picture) - A copy of the original that will have the
        kernel applied to it.
    x (type: int) - The x value of the pixel to modify
    y (type: int) - The y value of the pixel to modify
    kernel (type: 2D list of int) - The kernel to apply.
    """

    # accumulator variables
    red_sum = 0
    green_sum = 0
    blue_sum = 0

    for i in range(-1, 2):
        for j in range(-1, 2):
            x = x + j
            y = y + i

            pixel = img.getPixel(x,y)
            red = pixel.getRed()
            green = pixel.getGreen()
            blue = pixel.getBlue()
          
            red_sum += red * kernel[i+1][j+1]
            green_sum += green * kernel[i+1][j+1]
            blue_sum += blue * kernel[i+1][j+1]

#Red check
    if 0 > red_sum:
        red_sum = 0
    elif 255 < red_sum:
        red_sum = 255

#Green check
    if 0 > green_sum:
        green_sum = 0
    elif 255 < green_sum:
        green_sum = 255

#Blue check
    if 0 > blue_sum:
        blue_sum = 0
    elif 255 < blue_sum:
        blue_sum = 255

 
    pixel = filtered_img.getPixel(x,y)
    pixel.setRed(red_sum)
    pixel.setGreen(green_sum)
    pixel.setBlue(blue_sum)


def convolution(img, kernel):
    """
    Performs convolution on all non-border pixels in the img, using the given
    convolution kernel.

    Params:
    img (type: Picture) - The picture to modify.
    kernel (type: 2D list of int) - The kernel to apply.
    """

    # Makes a copy of the original image. This copy will be modified while the
    # original will remain unchanged.
    filtered_img = img.copy()

    # Avoids border pixels
    width = img.getWidth()
    height = img.getHeight()
    for x in range(1, width - 1):
        for y in range(1, height - 1):
            
            apply_kernel(img, filtered_img, x, y, kernel)

    return filtered_img



def flip_filter(img):
    """
    Flips image upside down

    Parameters:
    img(type: Image)

    Returns
    img_copy(Type: image)
    
    """

    img_copy = img.copy()
    w = img_copy.getWidth()
    h = img_copy.getHeight()
    for x in range(w):
        for y in range(h//2):
            top_pix = img.getPixel(x,y)
            bottom_pix = img.getPixel(x,h-1-y)
            img_copy.setPixel(x,h-1-y, top_pix)
            img_copy.setPixel(x,y,bottom_pix)

    for x in range(w):
        for y in range(-h//2):
            top_pix = img.getPixel(x,y)
            bottom_pix = img.getPixel(x,h-1-y)
            img_copy.setPixel(x,h-1-y, top_pix)
            img_copy.setPixel(x,y,bottom_pix)

    return img_copy


def mirror_x(img):
    """ 
    Mirrors image over x axis

    Parameters:
    img(type: Image)

    Returns
    img_copy(Type: image)

    """

    img_copy = img.copy()
    w = img_copy.getWidth()
    h = img_copy.getHeight()
    for x in range(w):
        for y in range(h//2):
            top_pix = img_copy.getPixel(x,y)
            bottom_pix = img_copy.getPixel(x,h-1-y)
            img_copy.setPixel(x,h-1-y, top_pix)
            img_copy.setPixel(x,y,bottom_pix)


    return img_copy


def mirror_filter(img):

    """
    Mirrors image over the y axis

    Parameters:
    img(type: Image)

    Returns
    img_copy(Type: image)
    """

    img_copy = img.copy()
    w = img_copy.getWidth()
    mirror_pt = w // 2
    for y in range(img_copy.getHeight()):
        for x in range(mirror_pt):
            left_pix = img_copy.getPixel(x,y)
            right_pix = img_copy.getPixel(w-1-x,y)
            img_copy.setPixel(w-1-x,y,left_pix)
            img_copy.setPixel(x,y,right_pix)
    
    return img_copy

def gray_filter(img):

    """
    Creates filter that applies a gray filter

    Parameters:
    img(type: Image)

    Returns
    img_copy(Type: image)
    """

    img_copy = img.copy()
    x = img_copy.getHeight()
    for row in range(x):
        for col in range(img_copy.getWidth()):
            p = img_copy.getPixel(col,row)

            red = p.getRed()
            green = p.getGreen()
            blue = p.getBlue()

            gray = int((red + green + blue)/3)
            p.setRed(gray)
            p.setGreen(gray)
            p.setBlue(gray)

    return img_copy

def create_filtered_pics(img):
    """
    Creates a tuple of photos with the given filters applied

    Parameters:
    img(type: Image)

    Returns
    img_tuple(Type: tuple)
    """

    img_tuple = (unique_filter(img), convolution(img, [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]), flip_filter(img), mirror_filter(img), mirror_x(img), gray_filter(img))
    return img_tuple



def assemble_collage(filtered_pics):
    """
    Assembles a collage of six filtered pictures.
    
    Parameters
    filtered_pics(type: tuple)

    Returns
    collage(type: image)
    """
    # Create a new canvas picture

    x = filtered_pics[0].getWidth()
    y = filtered_pics[0].getHeight()
    collage = comp110_image.Picture(x * 3, y * 2)

    copy_to(filtered_pics[0], collage, 0, 0)
    copy_to(filtered_pics[1], collage, x, 0)
    copy_to(filtered_pics[2], collage, x * 2, 0)
    copy_to(filtered_pics[3], collage, x, y)
    copy_to(filtered_pics[4], collage, 0, y)
    copy_to(filtered_pics[5], collage, x * 2, y)

    return collage

    

def shrink(img, scale_factor):
    """
    shrinks image

    Parameters:
    img(type: Image)

    scale_factor(type: int)

    Returns
    shrunk_image(Type: image)

    """
    shrunk_img = comp110_image.Picture(img.getWidth() // scale_factor, img.getHeight() // scale_factor)

    for x in range(shrunk_img.getWidth()):
        for y in range(shrunk_img.getHeight()):
            scale_x = x * scale_factor
            scale_y = y * scale_factor

            scaled_pixel = img.getPixel(scale_x, scale_y)
            shrunk_img.setPixel(x, y, scaled_pixel) 

    return shrunk_img

def get_shrink_factor(img, max_w, max_h):

    """
    Gets shrink factor for image

    Parameters:
    img(type: Image)

    max_w(type: int)

    max_h(type: int)

    Returns
    a(Type: int)
    """
    
    w = math.ceil(img.getWidth() / max_w)
    h = math.ceil(img.getHeight() / max_h)

    a = max(w, h)
    print(a)

    if a == 0:
        a = 1
    
    return a 


def main():
    """
    starts program

    Parameters
    None

    Returns:
    Collage(type: image)
    """
    image_filename = input("Enter the name of a picture file: ")
    copy_file = input("Enter the filename you will save the collage to")
    w = int(input("Enter the maximum width of the collage: "))


    while w < 3:
        w = int(input("Enter the maximum width of the collage: "))

    h = int(input("Enter the maximum height of the collage: "))

    while h < 1:
        h = int(input("Enter the maximum height of the collage: "))
    
    pic = comp110_image.Picture(filename= image_filename)
    shrink_dim = get_shrink_factor(pic, w // 3, h // 2)
    shrink_pic = shrink(pic, shrink_dim)
    pics = create_filtered_pics(shrink_pic)
    collage = assemble_collage(pics)

    collage.show()
    collage.save(copy_file)

if __name__ == "__main__":
    
    main()
