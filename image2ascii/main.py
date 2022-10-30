#!/usr/bin/bash

import cv2
import matplotlib.pyplot as plt
import numpy as np
# import rembg

import argparse

def main(image_path, im_size=100, rm_bg=False, invert=False, save_to=None):

    density = "Ñ@#W$9876543210?!abc;:+=-,._"
    density = density + " "*(51-len(density))
    if invert:
        density = density[::-1]

    # Pixel to ASCII Mapping
    pix2asc = {i : density[i] for i in range(0, 255//5)}
    def get_ascii(value):
        idx = int(value // 5)
        if idx == 51:
            idx -= 1
        return(pix2asc[idx])


    # Read image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Resize and convert to grayscale (for example by taking the mean)
    h = int(image.shape[0] / (image.shape[0] // im_size))
    w = int(image.shape[1] / (image.shape[1] // im_size))
    image = cv2.resize(image, (h,w), interpolation = cv2.INTER_AREA)
    # could take the mean
    # image = np.mean(image, axis=2)
    # or use cv2's algorithm
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # # Remove image background
    # if rm_bg:
    #     image = rembg.remove(image)

    plt.imshow(image); plt.show();

    # Map pixels to ASCII
    u, inv = np.unique(image, return_inverse=True)
    output = np.array([get_ascii(p) for p in u])[inv].reshape(image.shape)

    # save to file
    if save_to is not None:
        with open(save_to, "w") as f:
            for row in output:
                for char in row:
                    char = char + " "
                    f.write(char)
                f.write("\n")
    else:
        # print to screen
        for row in output:
            for char in row:
                print(char, end=" ")
            print("")
    



if __name__=='__main__':
    parser = argparse.ArgumentParser(
        prog="Image-2-ASCII",
        description="Convert image to ASCII-art"
    )
    parser.add_argument("filename", metavar="str", type=str, 
                        help="path to an image file.")
    parser.add_argument("-s", "--size", metavar="int", type=int, default=40,
                        help="size to resize image to (height = width). default=40.")
    parser.add_argument("-i", "--invert", action="store_true", default=False,
                        help="invert pixel to ascii mapping.")
    parser.add_argument("-o", "--output", metavar="str", default=None,
                        help="a file to save the ASCII output to.")
                        

    # parser.add_argument("-k", "--keep_background", action="store_true",
    #                     default=False, 
    #                     help="use flag to keep image backround. default is remove background."
    #                     )


    args=parser.parse_args()

    # "C:\\Users\\hanse\\OneDrive\\Pictures\\me.jpg"
    main(args.filename, im_size=args.size, invert=args.invert, save_to=args.output)