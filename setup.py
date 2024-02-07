from setuptools import setup

setup(
    author='Ryan Hamilton',
    author_email='ryan.hamilton@ec.gc.ca',
    name='ee_data_eng',
    version='0.1.0',
    package_dir={'': 'src'},
    install_requires=[
        'click',
        'geopandas',
        'pandas'
    ],
    entry_points='''
        [console_scripts]
        ee_data_eng=ee_data_eng:cli
    '''
)