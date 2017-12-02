from setuptools import setup

with open('requirements.txt') as f:
    requirements = [l.split(' ')[0] for l in f.readlines()]


setup(name='pyne-xmas-elves',
      version='0.2',
      description='The Great Elf Game adapted for Python North East - client & server',
      url='http://github.com/pythonnortheast/xmas-elves',
      author='Scott Walton',
      author_email='scott@pythonnortheast.com',
      license='MIT',
      packages=['server.elves'],
      python_requires='>=3.5',
      install_requires=requirements,
      zip_safe=False)
