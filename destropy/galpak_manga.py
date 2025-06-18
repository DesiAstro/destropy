import galpak
from galpak import GalPaK3D


def run_galpak_fit(
    flux_cube_path: str,
    var_cube_path: str,
    redshift: float,
    lsf_fwhm: float = 1.67,
    psf_fwhm: float = 2.45,
    psf_pa: float = 0.0,
    psf_ba: float = 1.0,
    max_iterations: int = 15000,
    output_prefix: str = 'galpak_fit_output',
    overwrite: bool = True,
    verbose: bool = True,
    mcmc_method: str = 'multinest',
    mcmc_sampling: str = 'Cauchy'
):
   
    model = galpak.DiskModel(
        flux_profile='exponential',
        thickness_profile='gaussian',
        dispersion_profile='thin',
        rotation_curve='NFW',
        redshift=redshift,
        cosmology='Planck15'
    )

    instrument = galpak.MANGA(
        lsf_fwhm=lsf_fwhm,
        psf_fwhm=psf_fwhm,
        psf_pa=psf_pa,
        psf_ba=psf_ba
    )

    gk = galpak.run(
        flux_cube_path,
        var_cube_path,
        instrument=instrument,
        model=model,
        max_iterations=max_iterations,
        verbose=verbose,
        mcmc_method=mcmc_method,
        mcmc_sampling=mcmc_sampling
    )

    gk.save('out_test_NFW', overwrite=overwrite)

    return gk


