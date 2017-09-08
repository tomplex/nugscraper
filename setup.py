from setuptools import setup

setup(
    name='nugscraper',
    version='0.1.0',
    packages=['nugscraper'],
    url='https://github.com/tomplex/nugscraper',
    license='MIT',
    author='Tom Caruso',
    author_email='carusot42@gmail.com',
    keywords=['command line', 'live music', 'nugs'],
    description='Command-line tool to bulk download files from nugs.net',
    entry_points={
        'console_scripts': [
            'nugscraper = nugscraper.main:nugscraper'
        ]
    }
)

