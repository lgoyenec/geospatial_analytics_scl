from setuptools import setup, find_packages

setup(
    name             = 'geospatial_analytics_scl',
    version          = '0.1',
    packages         = find_packages(where = 'src'),
    package_dir      = {'': 'src'},
    install_requires = [
        'boto3',
        'bs4',
        'dotenv',
        'fiona',
        'geopandas',
        'h3',
        'io',
        'matplotlib',
        'numpy',
        'pandas',
        'requests',
        'shapely',
        'sodapy',
        'urllib'
    ],
)
