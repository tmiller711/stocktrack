from setuptools import setup, find_packages

setup(
    name='stocktrack',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'click',
        'requests',
        'pandas',
        'matplotlib',
        'colorama'
    ],
    entry_points='''
    [console_scripts]
    stocktrack=stocktrack:main
    '''
    )
