#!/usr/bin/env python3

import cv2
import matplotlib.pyplot as plt
import numpy as np
import rembg

import argparse

def main(image_path, resize_factor=1, rm_bg=False, invert=False, save_to=None):

    density = " _.,-=+:;cba!?0123456789$W#@N" #since pixel value of 0 = black, let's start with " "
    # density = " .:░▒▓█"  #Ñ
    if invert:
        density = density[::-1]
    # density = density + " "*(51-len(density))

    # Pixel to ASCII Mapping
    range_size = 9 #255 // 9 = len(density) - 1
    pix2asc = {i : density[i] for i in range(0, len(density))}
    def get_ascii(value):
        idx = int(value // range_size)
        return(pix2asc[idx])

    # Read image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Resize and convert to grayscale (for example by taking the mean)
    h = image.shape[0] // resize_factor
    w = image.shape[1]// resize_factor
    # w = int(image.shape[1] / (image.shape[1] // im_size))
    image = cv2.resize(image, (w, h), interpolation = cv2.INTER_AREA)
    
    # could take the mean : image = np.mean(image, axis=2)
    # or use cv2's rgb to gray algorithm
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image = image + (255 - np.max(image))

    # Remove image background
    if rm_bg:
        image = rembg.remove(image)
        image = image[:, :,0] 

    # plt.imshow(image, cmap="bone"); plt.show();

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
                        help="path to the image file to convert to ASCII.")
    parser.add_argument("-s", "--scale", metavar="int", type=int, default=2,
                        help="scale down height and width of image by this factor.")
    parser.add_argument("-i", "--invert", action="store_true", default=False,
                        help="invert pixel value to ascii mapping.")
    parser.add_argument("-o", "--output", metavar="str", default=None,
                        help="-o FILENAME. Specify a file to save the ASCII output to.")                        
    parser.add_argument("-r", "--remove_background", action="store_true",
                        default=False, 
                        help="use flag to automatically remove image backround. default is False. removes background using 'rembg' library."
                        )


    args=parser.parse_args()
    # "C:\\Users\\hanse\\OneDrive\\Pictures\\me.jpg"
    main(args.filename, resize_factor=args.scale, invert=args.invert, save_to=args.output, rm_bg=args.remove_background)