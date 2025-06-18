
# cube_animator.py

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from tqdm import tqdm
import imageio.v2 as imageio
from io import BytesIO


# generates data cube image animation

def generate_cube_animation_image(fits_file,gif_name="cube_animation.gif",duration=0.05,cmap='jet',start=0,stop=None,step=1):
    """Generate GIF from FITS cube directly using plt interface (no intermediate images)."""

    # Open FITS and read data
    cube = fits.open(fits_file)
    data = cube['FLUX'].data
    cube.close()

  

    

    frames = []

    for i in tqdm(range(data.shape[0]), desc="Generating frames"):
        plt.figure(figsize=(6, 5))
        plt.imshow(data[i,:,:], cmap=cmap, origin='lower')
        plt.title(f"Slice z = {i}")
        plt.axis('off')

        # Save current figure to in-memory buffer
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        buf.seek(0)
        frames.append(imageio.imread(buf))
        buf.close()

    # Save all frames as GIF
    imageio.mimsave(gif_name, frames, duration=duration)
    print(f"GIF image of data cube saved as: {gif_name}")


# generates data cube spectral animation

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from tqdm import tqdm
import imageio.v2 as imageio
from io import BytesIO

def generate_cube_animation_spectral(fits_file, gif_name="cube_animation.gif", duration=0.1):
   
    with fits.open(fits_file) as cube:
        data = cube['FLUX'].data  # shape (n_wave, n_y, n_x)
        wave = cube['WAVE'].data

  

    frames = []

    for y in tqdm(range(data.shape[1])):
         for x in tqdm(range(data.shape[2])):
            spectrum = data[:, y, x]

            plt.figure(figsize=(6, 4))
            plt.plot(wave, spectrum, color='blue')
            plt.xlabel("Spectral Pixel")
            plt.ylabel("Flux")
            plt.title(f"Spectrum at (x={x}, y={y})")
            plt.grid(True)
            plt.tight_layout()

            buf = BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            buf.seek(0)
            frames.append(imageio.imread(buf))
            buf.close()

    imageio.mimsave(gif_name, frames, duration=duration)
    print(f"GIF spectral of data cube saved as: {gif_name}")

