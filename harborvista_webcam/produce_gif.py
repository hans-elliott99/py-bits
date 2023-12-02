from PIL import Image
import imageio

from time import localtime, strftime
import numpy as np
import requests
from io import BytesIO

import sys


def scrape_frames(n_frames=30):
    """
    Get latest frame from the web cam URL. Repeat n_frames times and save in list.
    For 30 frames, time ~= 1m 25.5s
    """
    frames = []
    for i in range(n_frames):
        response = requests.get("https://apps.lanecounty.org/LCWebCams/HarborVista")
        frames += [np.array( Image.open(BytesIO(response.content)).convert('RGB') )]
        sys.stdout.write("\r frame {0} ".format(str(i+1)))
        #sys.stdout.flush()

    return frames


if __name__ == '__main__':
    if len(sys.argv) > 1:
        n_frames = int(sys.argv[1])
    else:
        n_frames = 30
    
    imageio.mimsave(f'C:/Users/hanse/Documents/py-bits/harborvista_webcam/gifs/{strftime("%m-%d_%H.%M", localtime())}_frames.gif', 
                    scrape_frames(n_frames),
                    fps=0.75)

