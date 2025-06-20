# destropy/core.py


import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy import units as u
from specutils import Spectrum1D
from specutils.fitting import fit_generic_continuum
import warnings

warnings.filterwarnings("ignore")


# Read manga LINCUBE and Extract IVAR  Cube
# it takes input as a FITS cube. lower and higher index limit of(x,y,z) axis 
# return output as VARIANCE(VAR) cube
def crop_variance(input_fits: str, output_fits: str,x1:int,x2:int,y1:int,y2:int, z1: int, z2: int):
    file = fits.open(input_fits)
    ivar_cube = file['IVAR'].data
    var_cube=1/ivar_cube
    crop_cube_var = var_cube[z1:z2, y1:y2, x1:x2]
    
    fits.writeto(output_fits, crop_cube_var, overwrite=True, header=file['IVAR'].header)
    print(f"crop_extracted_variance cube saved to {output_fits}")
    print('Cube after crop:', crop_cube_var.shape)
    
    

# subtracts a single continuum from a single data cube
#Takes input as MANGA data cube
# Return output as Continuum subtracted data cube


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
    
    
#Takes input as list of MANGA data cube
# Return output aslist  Continuum subtracted data cube

def subtract_continuum_list(input_fits_list: list, output_fits_list: list):
    """
    Subtract the continuum from multiple FITS cubes and save the continuum-subtracted cubes.

    Parameters:
    - input_fits_list: list of input FITS file 
    - output_fits_list: list of output FITS file 
    """
    
    # Ensure the number of input and output files match
    if len(input_fits_list) != len(output_fits_list):
        raise ValueError("The number of input FITS files must match the number of output FITS files.")
    
    for input_fits, output_fits in zip(input_fits_list, output_fits_list):
        # Open the FITS file and extract flux and wavelength
        with fits.open(input_fits) as file:
            flux_cube = file['FLUX'].data
            lam = file['WAVE'].data
            wavelength = lam * u.AA

            continuum_cube = np.zeros_like(flux_cube)
            cont_sub_cube = np.zeros_like(flux_cube)

            # Process each pixel in the flux cube
            for y in range(flux_cube.shape[1]):
                for x in range(flux_cube.shape[2]):
                    flux = flux_cube[:, y, x] * u.Unit('1e-17 erg / (cm2 s Angstrom)')
                    spectrum = Spectrum1D(spectral_axis=wavelength, flux=flux)
                    fitted_continuum = fit_generic_continuum(spectrum)
                    continuum = fitted_continuum(wavelength)
                    continuum_cube[:, y, x] = continuum.value
                    cont_sub_cube[:, y, x] = (flux - continuum).value

            # Write the continuum-subtracted cube to the output FITS file
            fits.writeto(output_fits, cont_sub_cube, overwrite=True, header=file['FLUX'].header)
            print(f"Continuum-subtracted cube saved to {output_fits}")
   
    
    
    
    
    
    
    
    
  # It takes input as a FITS cube. lower and higher index limit of(x,y,z) axis 
# return output as crop cube or sub-cube(x1,y1,z1) from bigger cube(x,y,z)

def crop_cube(input_fits: str, output_fits: str,x1:int,x2:int,y1:int,y2:int, z1: float, z2: float):
    file = fits.open(input_fits)
    flux_cube = file['FLUX'].data
    print('Cube before crop:', flux_cube.shape)
    crop_cube_z = flux_cube[z1:z2, y1:y2, x1:x2]
    print('Cube after crop:', crop_cube_z.shape)
    fits.writeto(output_fits, crop_cube_z, overwrite=True, header=file['FLUX'].header)
    print(f"Cropped cube saved to {output_fits}")



#Takes input as MAMGA FITS Data cube
#Return output as particular (x,y) spaxel
def plot_spaxel_spectra(input_fits: str, x: int, y: int):
    file = fits.open(input_fits)
    flux_cube = file['FLUX'].data
    lam = file['WAVE'].data
    plt.figure()
    plt.plot(lam, flux_cube[:, y, x])
    plt.xlabel("Wavelength (Angstrom)")
    plt.ylabel("Flux")
    plt.title(f"Spaxel Spectrum at ({x}, {y})")
    plt.show()
    print(lam)
	
#Takes input as MAMGA FITS Data cube
#Return output as particular flux map at given z or wavelength

def plot_flux_map(input_fits: str, lam_index: int):
    file = fits.open(input_fits)
    flux_cube = file['FLUX'].data
    lam = file['WAVE'].data
    plt.figure()
    plt.imshow(flux_cube[lam_index, :, :], origin='lower', cmap='viridis')
    plt.colorbar(label='Flux')
    plt.title(f"Flux Map at Wavelength Index")
    plt.show()




    
	
	
