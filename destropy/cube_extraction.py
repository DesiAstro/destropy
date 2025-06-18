"""
These line code extract SDSS MANGA all flux map images/all spaxel spectra and  saves into png/pdf file
"""
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from tqdm import tqdm





def save_flux_map(input_fits: str, cmap: str = 'viridis'):
    # Open FITS and read data
    cube= fits.open(input_fits) 
    data = cube['FLUX'].data

    # Loop through each slice in the data cube
    for i in tqdm(range(data.shape[0]), desc='Saving flux maps'):
        plt.figure(figsize=(6, 5))
        plt.imshow(data[i, :, :], cmap=cmap, origin='lower')
        plt.title(f"Slice z = {i}")
        plt.xlabel('X-Spaxel')
        plt.ylabel('Y-Spaxel')  
        plt.colorbar(label='Flux')
        plt.tight_layout()
        plt.savefig(f'flux_map_z_{i}.png')
        plt.close()  



def save_spectral_map(input_fits: str):
    # Open FITS and read data
    cube= fits.open(input_fits) 
    data = cube['FLUX'].data
    wave=cube['WAVE'].data

    # Loop through each slice in the data cube
    for y in tqdm(range(data.shape[0])):
        for x in tqdm(range(data.shape[1])):
            plt.figure(figsize=(6, 5))
            plt.plot(wave,data[:,y,x])
            plt.title(f"Slice  = {x}{y}")
            plt.xlabel('X-Spaxel')
            plt.ylabel('Y-Spaxel') 
            
            plt.tight_layout()
            plt.savefig(f'flux_map__{x}_{y}.png')
            plt.close()  

