from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(name              = 'FriendlyELEC_NanoHatMotor',
      version           = '1.0.0',
      author            = 'Limor Fried(Adafruit), FriendlyELEC',
      author_email      = 'support@friendlyarm.com',
      description       = 'Library for FriendlyELEC NanoHat Motor',
      license           = 'MIT',
      url               = 'https://github.com/friendlyarm/NanoHAT-Motor-Python-Library',
      dependency_links  = ['https://github.com/adafruit/Adafruit_Python_GPIO/tarball/master#egg=Adafruit-GPIO-0.7'],
      install_requires  = ['Adafruit-GPIO>=0.7'],
      packages          = find_packages())
