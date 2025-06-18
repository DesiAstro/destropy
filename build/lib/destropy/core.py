# destropy/core.py

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import specutils
from astropy import units as u
from specutils import Spectrum1D
from specutils.fitting import fit_generic_continuum
import warnings

warnings.filterwarnings("ignore")

def subtract_continuum(input_fits: str, output_fits: str):
	file = fits.open(input_fits)
    	flux_cube = file['FLUX'].data
    	lam = file['WAVE'].data
    	wavelength = lam * u.AA

    	continuum_cube = np.zeros_like(flux_cube)
    	cont_sub_cube = np.zeros_like(flux_cube)

    	for y in range(flux_cube.shape[1]):
        	for x in range(flux_cube.shape[2]):
            		flux = flux_cube[:, y, x] * u.Unit('1e-17 erg / (cm2 s Angstrom)')
            		spectrum = Spectrum1D(spectral_axis=wavelength, flux=flux)
            		fitted_continuum = fit_generic_continuum(spectrum)
            		continuum = fitted_continuum(wavelength)
            		continuum_cube[:, y, x] = continuum.value
            		cont_sub_cube[:, y, x] = (flux - continuum).value

    fits.writeto(output_fits, cont_sub_cube, overwrite=True, header=file['FLUX'].header)
    print(f"Continuum-subtracted cube saved to {output_fits}")


def crop_cube(input_fits: str, output_fits: str, z1: int, z2: int):
	file = fits.open(input_fits)
    	flux_cube = file['FLUX'].data
    	lam = file['WAVE'].data
    	print('cube before crop', flux_cube.shape)
    	crop_cube_z = flux_cube[z1:z2, :, :]
    	print('cube after crop', crop_cube_z.shape)
    	fits.writeto(output_fits, crop_cube_z, overwrite=True, header=file['FLUX'].header)
    	print(f"Cropped cube saved to {output_fits}")



def plot_spaxel_spectra(input_fits: str,x_spaxel:int,y_spaxel:int):
	file = fits.open(input_fits)
	flux_cube = file['FLUX'].data
        lam = file['WAVE'].data
        print(lam)
    
def plot_flux_map(input_fits: str,lam:int):
	file = fits.open(input_fits)
	flux_cube = file['FLUX'].data
        lam = file['WAVE'].data
        plt.plot(lam,flux_cube[lam,:,:]
    
	
	
