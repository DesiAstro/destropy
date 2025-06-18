from setuptools import setup, find_packages

setup(
    name='destropy',
    version='0.1.0',
    date='17-04-2025',
    author='Jyoti Prakash',
    description='A library for SDSS MaNGA data cube manipulation and Analysis',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'astropy',
        'specutils',
        'matplotlib',
    ],
    python_requires='>=3.9',
)


