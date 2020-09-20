from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='luna',
    version='0.1.0',
    description='Digital assistant for everyday use',
    long_description=readme,
    author='Clayton Henderson',
    author_email='clayhenderson87@gmail.com',
    url='https://github.com/adamantius7877/Luna',
    license=license,
    packages=find_packages(exclude=('tests','docs'))
)
