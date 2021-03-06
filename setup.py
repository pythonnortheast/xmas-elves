from os import path
from setuptools import setup
import m2r

with open(path.abspath('requirements.txt')) as f:
    requirements = [l.split(' ')[0] for l in f.readlines()]

readme_file = path.join(path.dirname(path.abspath(__file__)),
                        'README.md')
try:
    DESCRIPTION = m2r.parse_from_file(readme_file)
except (IOError, FileNotFoundError):
    DESCRIPTION = ''

setup(name='pyne-xmas-elves',
      version='0.7.1',
      description='The Great Elf Game adapted for Python North East - client '
      '& server',
      url='http://github.com/pythonnortheast/xmas-elves',
      author='Scott Walton',
      author_email='scott@pythonnortheast.com',
      license='MIT',
      long_description=DESCRIPTION,
      packages=['pyne_xmas_elves.client', 'pyne_xmas_elves.server'],
      python_requires='>=3.5',
      install_requires=requirements,
      scripts=['bin/elves.py'],
      zip_safe=False)
