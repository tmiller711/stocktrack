from setuptools import setup, find_packages

setup(
    name='stocktrack',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'click',
        'requests'
    ],
    entry_points='''
    [console_scripts]
    stocktrack=main:main
    '''
    )
