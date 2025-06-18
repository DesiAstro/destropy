import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy import units as u
from specutils import Spectrum1D
from specutils.fitting import fit_generic_continuum

def plot_sdss_spectrum(input_fits:str):
    
    
    # Open the FITS file
    hdul=fits.open(input_fits)
    
        # 
    data = hdul[1].data
    header = hdul[0].header

        # Get flux and log-wavelength
    flux = data['flux']
    loglam = data['loglam']
    wavelength = 10**loglam  #  loglam to linear scale

    # Plot the spectrum
    plt.figure()
    plt.plot(wavelength, flux, color='blue', lw=0.7)
    plt.xlabel('Wavelength (Å)')
    plt.ylabel('Flux (10^-17 erg/s/cm^2/AA)')
    plt.show()
    
    
def plot_sdss_image(input_fits:str):
    hdul=fits.open(input_fits)
    flux=hdul['FLUX']
    plot.imshow(flux,origin='lower')
    plt.colorbar()
    plt.show()
    
  
"""
 This line of code uses SDSS spectra input file and returns comntinuum subtracted fits file
"""
def sdss_continuum(input_file: str, output_file: str):
    hdul = fits.open(input_file)
    
    data = hdul[1].data
    header = hdul[0].header
    
    flux = data['flux'] * u.Unit('1e-17 erg / (cm2 s Angstrom)')
    loglam = data['loglam']
    wavelength = (10 ** loglam) * u.AA

    spectrum = Spectrum1D(spectral_axis=wavelength, flux=flux)

    fitted_continuum = fit_generic_continuum(spectrum)
    continuum = fitted_continuum(wavelength)

    cont_sub_spectra = (flux - continuum).value

    # Save as FITS with header
    hdu = fits.PrimaryHDU(data=cont_sub_spectra, header=hdul[1].header)
    hdu.writeto(output_file, overwrite=True)

    print(f"Continuum-subtracted SDSS spectra saved to {output_file}")

    
    
    
    
    
    

