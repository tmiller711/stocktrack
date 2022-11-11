from setuptools import setup, find_packages 

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='stocktrack',
    version='0.0.5',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'click',
        'requests',
        'pandas',
        'matplotlib',
        'colorama',
    ],
    entry_points='''
    [console_scripts]
    stocktrack=cli.stocktrack:main
    ''',
    include_package_data=True,
    package_data={'': ['backtests', 'results']},
    )
