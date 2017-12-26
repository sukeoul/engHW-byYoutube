from setuptools import setup
from bhm import __init__

setup(name='engHW',
      version="0,0,1",
      description='Giving english homework using youtube video',
      install_requires=[
            'gspread',
            'oauth2client',
            'selenium'
      ])