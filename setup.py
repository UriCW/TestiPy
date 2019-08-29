from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='TestiPy',
      version='0.1',
      description='A mocking framework for pytest',
      url='https://gitlab.com/IM_Uri/common',
      author='Uri Cohen',
      author_email='Uri@example.com',
      license='MIT',
      packages=['Testi'],
      install_requires=requirements,
      zip_safe=False)
